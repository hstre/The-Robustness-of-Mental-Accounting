"""Compare variants on the same footing: first 3 runs of every model, all runs pooled.

The base condition has 10-15 runs per model, the variants 3; with the +0.5 correction
the size of a log OR depends on n, so base is restricted to participant_id < 3 here.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .analysis import EFFECTS, HUMAN_POOLED, apply_exclusions, descriptives, load_raw, model_effects
from .variants import VARIANTS

ORDER = ["base", "neutral", "rational", "paraphrase", "between"]


def compare(raw_root: Path, out_dir: Path, n_per_model: int = 3, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    eff_rows, desc_rows = [], []
    for name in ORDER:
        d = raw_root if name == "base" else raw_root / name
        if not any(d.glob("*.jsonl")):
            continue
        v = VARIANTS[name]
        df = apply_exclusions(load_raw(d))
        df = df[df["included"] & (df["participant_id"] < n_per_model)]
        for eff, (e, se) in model_effects(df, rng, v.items).items():
            eff_rows.append({"variant": name, "effect": eff, "estimate": e, "se": se})
        desc_rows.append({"variant": name, "n_runs": len(df), **descriptives(df, v.items)})
    eff = pd.DataFrame(eff_rows)
    wide = eff.pivot(index="effect", columns="variant", values="estimate").loc[EFFECTS]
    wide = wide[[c for c in ORDER if c in wide.columns]]
    wide["humans"] = [HUMAN_POOLED[e][0] for e in wide.index]
    desc = pd.DataFrame(desc_rows).set_index("variant").T
    out_dir.mkdir(parents=True, exist_ok=True)
    eff.to_csv(out_dir / "variants_effects_long.csv", index=False)
    wide.to_csv(out_dir / "variants_effects.csv")
    desc.to_csv(out_dir / "variants_descriptives.csv")
    (out_dir / "variants.md").write_text(
        f"# Variants compared (first {n_per_model} runs per model, all models pooled)\n\n"
        "Effect estimates (same metrics as the paper; CIs ignore clustering by model):\n\n"
        + wide.to_markdown(floatfmt=".2f")
        + "\n\nResponse proportions / medians:\n\n" + desc.to_markdown(floatfmt=".2f") + "\n"
    )
    return wide
