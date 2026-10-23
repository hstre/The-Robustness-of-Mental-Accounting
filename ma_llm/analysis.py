"""Analysis mirroring Priolo et al. (2026), with models in place of countries.

Paper -> here:
* Unpooled per-country Bayesian regressions (N(0, 2.5) priors) -> per-model effect
  estimates with a +0.5 (Haldane-Anscombe) correction for binary outcomes, which
  plays the same role as the weakly informative prior (finite estimates when a
  model answers deterministically). Replication = 95% CI excludes 0 in the
  predicted direction, as in the paper.
* Hierarchical Bayesian meta-analysis across countries -> DerSimonian-Laird
  random-effects meta-analysis across models.
* Country-level MDS of standardized effect sizes -> the same on the model x
  scenario matrix (exploratory; only 12 rows).
GDP / demographic moderator analyses have no counterpart for LLMs and are omitted.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from .scenarios import FIN_LIT_CORRECT, QUALITY

# Pooled human estimates, Priolo et al. (2026), Table 3 (log OR for Game, Jacket,
# Play, Plane; evidence ratio for MrAB; Cohen's d for Drink and Gym).
HUMAN_POOLED = {
    "MrAB_gains": (1.48, 1.31, 1.65),
    "MrAB_losses": (2.13, 1.99, 2.27),
    "Game": (1.78, 1.54, 2.01),
    "Drink": (0.76, 0.66, 0.86),
    "Jacket": (0.53, 0.42, 0.63),
    "Play": (0.58, 0.41, 0.75),
    "Gym": (0.72, 0.50, 0.94),
    "Plane": (0.82, 0.69, 0.95),
}
METRIC = {
    "MrAB_gains": "evidence ratio", "MrAB_losses": "evidence ratio",
    "Game": "log OR", "Jacket": "log OR", "Play": "log OR", "Plane": "log OR",
    "Drink": "Cohen's d", "Gym": "Cohen's d",
}
EFFECTS = list(HUMAN_POOLED)
LOGIT_TO_D = math.sqrt(3) / math.pi  # Chinn (2000)
Z = stats.norm.ppf(0.975)


# Loading ------------------------------------------------------------------------

def load_raw(raw_dir: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(raw_dir.glob("*.jsonl")):
        for line in path.read_text().splitlines():
            if line.strip():
                rows.append(json.loads(line))
    if not rows:
        raise SystemExit(f"no data in {raw_dir}")
    return pd.DataFrame(rows)


def quality_score(answers: dict) -> int | None:
    a = (answers.get("Quality") or {}).get("answer")
    return QUALITY.options.index(a) + 1 if a in QUALITY.options else None


def apply_exclusions(df: pd.DataFrame) -> pd.DataFrame:
    """Paper: completion rate 100% and self-reported seriousness >= 4."""
    df = df.copy()
    df["quality"] = df["answers"].apply(quality_score)
    df["included"] = df["complete"] & (df["quality"] >= 4)
    return df


# Effect estimators ----------------------------------------------------------------

def _log_or(a: float, b: float, c: float, d: float) -> tuple[float, float]:
    """log OR for (a events / b non-events) vs (c events / d non-events), +0.5 corrected."""
    a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    return math.log(a * d / (b * c)), math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)


def log_or_binary(y1: np.ndarray, y0: np.ndarray) -> tuple[float, float]:
    """Effect of condition 1 vs condition 0 on P(y=1)."""
    return _log_or(y1.sum(), len(y1) - y1.sum(), y0.sum(), len(y0) - y0.sum())


def evidence_ratio(k: int, n: int) -> tuple[float, float]:
    """log odds of the predicted MrAB pattern relative to chance (1/9)."""
    p_k, p_n = k + 0.5, n - k + 0.5
    return math.log(p_k / p_n) - math.log(1 / 8), math.sqrt(1 / p_k + 1 / p_n)


def cohens_d(x1: np.ndarray, x0: np.ndarray) -> tuple[float, float]:
    n1, n0 = len(x1), len(x0)
    sp = math.sqrt(((n1 - 1) * x1.var(ddof=1) + (n0 - 1) * x0.var(ddof=1)) / (n1 + n0 - 2))
    if sp == 0:
        return float("nan"), float("nan")
    d = (x1.mean() - x0.mean()) / sp
    return d, math.sqrt((n1 + n0) / (n1 * n0) + d**2 / (2 * (n1 + n0)))


def game_effect(ans: pd.Series, rng: np.random.Generator, n_boot: int = 1000) -> tuple[float, float]:
    """P(price >= market value), stranger vs friend. 12 prices per participant, so the
    SE comes from a participant-level cluster bootstrap."""
    per_p = []
    for a in ans:
        st = fr = 0
        for c in ("Game1", "Game2", "Game3"):
            g = a[c]
            st += (g["stranger"] >= 5) + (g["stranger_face10"] >= 10)
            fr += (g["friend"] >= 5) + (g["friend_face10"] >= 10)
        per_p.append((st, fr))
    arr = np.array(per_p, dtype=float)  # events out of 6 per buyer type
    n = len(arr)

    def est(x: np.ndarray) -> float:
        s, f = x[:, 0].sum(), x[:, 1].sum()
        return _log_or(s, 6 * len(x) - s, f, 6 * len(x) - f)[0]

    point = est(arr)
    boots = [est(arr[rng.integers(0, n, n)]) for _ in range(n_boot)]
    se_boot = float(np.std(boots, ddof=1))
    # Floor: analytic SE treating each participant as one observation per buyer type.
    s, f = arr[:, 0].sum() / 6, arr[:, 1].sum() / 6
    se_floor = _log_or(s, n - s, f, n - f)[1]
    return point, max(se_boot, se_floor)


def answer_col(df: pd.DataFrame, item: str, key: str = "answer") -> pd.Series:
    return df["answers"].apply(lambda a: a[item][key])


def model_effects(df: pd.DataFrame, rng: np.random.Generator) -> dict[str, tuple[float, float]]:
    """All within-subjects effects for one model's included participants."""
    out = {}
    m1, m2, m3, m4 = (answer_col(df, f"MrAB{i}").to_numpy() for i in range(1, 5))
    n = len(df)
    out["MrAB_gains"] = evidence_ratio(int(((m1 == "A") & (m3 == "B")).sum()), n)
    out["MrAB_losses"] = evidence_ratio(int(((m2 == "A") & (m4 == "B")).sum()), n)
    out["Game"] = game_effect(df["answers"], rng)
    p1, p2 = answer_col(df, "Drink1", "price").to_numpy(), answer_col(df, "Drink2", "price").to_numpy()
    ok = (p1 > 0) & (p2 > 0)
    out["Drink"] = cohens_d(np.log(p1[ok]), np.log(p2[ok]))
    out["Jacket"] = log_or_binary(answer_col(df, "Jacket1").to_numpy() == "Yes",
                                  answer_col(df, "Jacket2").to_numpy() == "Yes")
    out["Play"] = log_or_binary(answer_col(df, "Play2").to_numpy() == "Yes",
                                answer_col(df, "Play1").to_numpy() == "Yes")
    # 1 = strongly agree ... 5 = strongly disagree; per-session payment (Gym1) should
    # produce more agreement with "I wasted $20" -> Gym2 - Gym1 > 0.
    out["Gym"] = cohens_d(answer_col(df, "Gym2", "wasted_20").to_numpy().astype(float),
                          answer_col(df, "Gym1", "wasted_20").to_numpy().astype(float))
    pay = "Pay your friend $35 for the coupon"
    out["Plane"] = log_or_binary(answer_col(df, "Plane1").to_numpy() == pay,
                                 answer_col(df, "Plane2").to_numpy() == pay)
    return out


def between_subjects_effects(df: pd.DataFrame) -> dict[str, tuple[float, float]]:
    """Paper's robustness check: only the condition each participant saw first."""
    specs = {
        "Jacket": ("Jacket1", "Jacket2", lambda a: a == "Yes"),
        "Play": ("Play2", "Play1", lambda a: a == "Yes"),
        "Plane": ("Plane1", "Plane2", lambda a: a == "Pay your friend $35 for the coupon"),
    }
    out = {}
    for eff, (c1, c0, f) in specs.items():
        first = df["order"].apply(lambda o: c1 if o.index(c1) < o.index(c0) else c0)
        y1 = df.loc[first == c1, "answers"].apply(lambda a: f(a[c1]["answer"])).to_numpy()
        y0 = df.loc[first == c0, "answers"].apply(lambda a: f(a[c0]["answer"])).to_numpy()
        out[eff] = log_or_binary(y1, y0) if len(y1) and len(y0) else (float("nan"),) * 2
    return out


def descriptives(df: pd.DataFrame) -> dict[str, float]:
    """Response proportions that make the effects interpretable for LLMs."""
    a = df["answers"]
    pay = "Pay your friend $35 for the coupon"
    out = {
        "MrAB1_A": (answer_col(df, "MrAB1") == "A").mean(),
        "MrAB2_A": (answer_col(df, "MrAB2") == "A").mean(),
        "MrAB3_B": (answer_col(df, "MrAB3") == "B").mean(),
        "MrAB4_B": (answer_col(df, "MrAB4") == "B").mean(),
        "Drink1_median": answer_col(df, "Drink1", "price").median(),
        "Drink2_median": answer_col(df, "Drink2", "price").median(),
        "Jacket1_yes": (answer_col(df, "Jacket1") == "Yes").mean(),
        "Jacket2_yes": (answer_col(df, "Jacket2") == "Yes").mean(),
        "Play1_yes": (answer_col(df, "Play1") == "Yes").mean(),
        "Play2_yes": (answer_col(df, "Play2") == "Yes").mean(),
        "Gym1_wasted20_mean": answer_col(df, "Gym1", "wasted_20").mean(),
        "Gym2_wasted20_mean": answer_col(df, "Gym2", "wasted_20").mean(),
        "Plane1_pay35": (answer_col(df, "Plane1") == pay).mean(),
        "Plane2_pay35": (answer_col(df, "Plane2") == pay).mean(),
        "Game_friend_median": a.apply(lambda x: np.median([x[c]["friend"] for c in ("Game1", "Game2", "Game3")])).median(),
        "Game_stranger_median": a.apply(lambda x: np.median([x[c]["stranger"] for c in ("Game1", "Game2", "Game3")])).median(),
        "fin_lit_mean": a.apply(lambda x: sum(x[k]["answer"] == v for k, v in FIN_LIT_CORRECT.items())).mean(),
    }
    return {k: float(v) for k, v in out.items()}


# Meta-analysis and MDS -------------------------------------------------------------

def dersimonian_laird(est: np.ndarray, se: np.ndarray) -> dict[str, float]:
    ok = np.isfinite(est) & np.isfinite(se) & (se > 0)
    y, v = est[ok], se[ok] ** 2
    k = len(y)
    if k == 0:
        return {"k": 0}
    w = 1 / v
    fe = (w * y).sum() / w.sum()
    q = (w * (y - fe) ** 2).sum()
    c = w.sum() - (w**2).sum() / w.sum()
    tau2 = max(0.0, (q - (k - 1)) / c) if k > 1 else 0.0
    wr = 1 / (v + tau2)
    mu = (wr * y).sum() / wr.sum()
    se_mu = math.sqrt(1 / wr.sum())
    i2 = max(0.0, (q - (k - 1)) / q) if q > 0 else 0.0
    return {"k": k, "estimate": mu, "ci_low": mu - Z * se_mu, "ci_high": mu + Z * se_mu,
            "tau": math.sqrt(tau2), "I2": i2, "p": 2 * stats.norm.sf(abs(mu / se_mu))}


def to_d(effect: str, x: float) -> float:
    return x if METRIC[effect] == "Cohen's d" else x * LOGIT_TO_D


def classical_mds(dist: np.ndarray, dims: int = 3) -> tuple[np.ndarray, np.ndarray]:
    n = dist.shape[0]
    j = np.eye(n) - np.ones((n, n)) / n
    b = -0.5 * j @ (dist**2) @ j
    vals, vecs = np.linalg.eigh(b)
    idx = np.argsort(vals)[::-1]
    vals, vecs = vals[idx], vecs[:, idx]
    pos = vals[vals > 0]
    coords = vecs[:, :dims] * np.sqrt(np.clip(vals[:dims], 0, None))
    return coords, vals[:dims] / pos.sum()


# Driver ------------------------------------------------------------------------------

def analyze(raw_dir: Path, out_dir: Path, families: dict[str, str] | None = None, seed: int = 1) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    families = families or {}
    df = apply_exclusions(load_raw(raw_dir))

    # Sample / data quality per model (analogue of the paper's exclusion reporting)
    samp = df.groupby("model").agg(
        n_started=("participant_id", "size"),
        n_complete=("complete", "sum"),
        n_included=("included", "sum"),
        cost_usd=("cost_usd", "sum"),
    )
    samp["family"] = samp.index.map(lambda m: families.get(m, ""))
    samp["parse_retry_rate"] = df.groupby("model")["pages"].apply(
        lambda s: np.mean([len(p["raw"]) > 1 for pages in s for p in pages]))
    samp.to_csv(out_dir / "sample.csv")

    inc = df[df["included"]]
    rows, between, desc = [], [], []
    for model, g in inc.groupby("model"):
        if len(g) < 2:
            continue
        for eff, (e, se) in model_effects(g, rng).items():
            rows.append({"model": model, "family": families.get(model, ""), "effect": eff,
                         "metric": METRIC[eff], "n": len(g), "estimate": e, "se": se,
                         "ci_low": e - Z * se, "ci_high": e + Z * se,
                         "replicated": bool(np.isfinite(e) and e - Z * se > 0)})
        for eff, (e, se) in between_subjects_effects(g).items():
            between.append({"model": model, "effect": eff, "estimate": e, "se": se,
                            "ci_low": e - Z * se, "ci_high": e + Z * se})
        desc.append({"model": model, **descriptives(g)})
    eff_df = pd.DataFrame(rows)
    eff_df.to_csv(out_dir / "effects_by_model.csv", index=False)
    pd.DataFrame(between).to_csv(out_dir / "between_subjects.csv", index=False)
    pd.DataFrame(desc).to_csv(out_dir / "descriptives.csv", index=False)

    # Pooled (random-effects) per effect, next to the human pooled estimate
    meta = []
    for eff in EFFECTS:
        sub = eff_df[eff_df["effect"] == eff]
        res = dersimonian_laird(sub["estimate"].to_numpy(), sub["se"].to_numpy())
        h = HUMAN_POOLED[eff]
        meta.append({"effect": eff, "metric": METRIC[eff], **res,
                     "replication_rate": sub["replicated"].mean() if len(sub) else float("nan"),
                     "human_estimate": h[0], "human_ci_low": h[1], "human_ci_high": h[2]})
    meta_df = pd.DataFrame(meta)
    meta_df.to_csv(out_dir / "meta.csv", index=False)

    # Similarity of each model's effect profile to the human pooled profile (in d units)
    wide = eff_df.pivot(index="model", columns="effect", values="estimate")[EFFECTS]
    wide_d = wide.apply(lambda col: col.map(lambda x: to_d(col.name, x)))
    human_d = np.array([to_d(e, HUMAN_POOLED[e][0]) for e in EFFECTS])
    prof = []
    for model, r in wide_d.iterrows():
        ok = r.notna().to_numpy()
        prof.append({"model": model,
                     "pearson_r_with_humans": stats.pearsonr(r.to_numpy()[ok], human_d[ok])[0] if ok.sum() > 2 else float("nan"),
                     "rmse_d_vs_humans": float(np.sqrt(np.mean((r.to_numpy()[ok] - human_d[ok]) ** 2))),
                     "mean_d": float(r.mean())})
    pd.DataFrame(prof).to_csv(out_dir / "profile_vs_humans.csv", index=False)

    # Exploratory MDS across scenarios (MrAB = mean of gains and losses, as in the paper)
    scen = wide_d.copy()
    scen["MrAB"] = scen[["MrAB_gains", "MrAB_losses"]].mean(axis=1)
    scen = scen[["MrAB", "Game", "Drink", "Jacket", "Play", "Gym", "Plane"]].dropna()
    mds_note = ""
    if len(scen) >= 4:
        z = (scen - scen.mean()) / scen.std(ddof=1).replace(0, np.nan)
        z = z.dropna(axis=1)
        x = z.to_numpy().T
        dist = np.sqrt(((x[:, None, :] - x[None, :, :]) ** 2).sum(-1))
        coords, share = classical_mds(dist)
        pd.DataFrame(coords, index=z.columns, columns=[f"dim{i+1}" for i in range(coords.shape[1])]).to_csv(out_dir / "mds_coordinates.csv")
        z.corr().to_csv(out_dir / "scenario_correlations_across_models.csv")
        mds_note = f"MDS variance share (dim1-3): {', '.join(f'{s:.1%}' for s in share)}"

    write_summary(out_dir, samp, eff_df, meta_df, mds_note)
    try:
        plot_forest(eff_df, meta_df, out_dir / "figure1_llm.png")
    except ImportError:
        pass


def write_summary(out_dir: Path, samp: pd.DataFrame, eff_df: pd.DataFrame, meta_df: pd.DataFrame, mds_note: str) -> None:
    lines = ["# Results: mental accounting in LLMs", "", "## Sample per model", "",
             samp.to_markdown(floatfmt=".3g"), "", "## Pooled effects (random effects across models) vs. humans", "",
             meta_df[["effect", "metric", "k", "estimate", "ci_low", "ci_high", "tau", "I2",
                      "replication_rate", "human_estimate", "human_ci_low", "human_ci_high"]].to_markdown(index=False, floatfmt=".2f"),
             ""]
    if len(eff_df):
        rep = eff_df.pivot(index="model", columns="effect", values="replicated")[EFFECTS]
        total = int(rep.to_numpy().sum())
        lines += ["## Unpooled replication (95% CI > 0 in predicted direction)", "",
                  f"Overall: {total}/{rep.size} effects ({total / rep.size:.1%}); humans: 133/147 (90.5%).", "",
                  rep.replace({True: "yes", False: "no"}).to_markdown(), ""]
    if mds_note:
        lines += ["## Exploratory MDS", "", mds_note, ""]
    (out_dir / "summary.md").write_text("\n".join(lines))


def plot_forest(eff_df: pd.DataFrame, meta_df: pd.DataFrame, path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 4.5))
    for i, eff in enumerate(EFFECTS):
        sub = eff_df[eff_df["effect"] == eff]
        jitter = np.linspace(-0.25, 0.25, len(sub)) if len(sub) > 1 else [0]
        ax.scatter(i + np.asarray(jitter), sub["estimate"], s=14, color="#9aa0a6", zorder=2,
                   label="Model" if i == 0 else None)
        m = meta_df[meta_df["effect"] == eff].iloc[0]
        if m.get("k", 0):
            ax.errorbar(i + 0.08, m["estimate"], yerr=[[m["estimate"] - m["ci_low"]], [m["ci_high"] - m["estimate"]]],
                        fmt="o", mfc="white", color="#1a7f7a", ms=8, mew=2, zorder=3,
                        label="LLM pooled" if i == 0 else None)
        ax.errorbar(i - 0.08, m["human_estimate"], yerr=[[m["human_estimate"] - m["human_ci_low"]], [m["human_ci_high"] - m["human_estimate"]]],
                    fmt="s", color="#3b2c85", ms=6, zorder=3, label="Humans pooled (Priolo et al.)" if i == 0 else None)
    ax.axhline(0, ls="--", color="black", lw=1)
    ax.set_xticks(range(len(EFFECTS)), [f"{e}\n({METRIC[e]})" for e in EFFECTS], fontsize=8)
    ax.set_ylabel("Effect estimate")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
