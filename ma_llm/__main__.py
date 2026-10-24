"""CLI: python -m ma_llm {check,estimate,preview,run,analyze} [options]"""

from __future__ import annotations

import argparse
import asyncio
import random
from pathlib import Path

import yaml

from .client import list_models
from .survey import get_item, item_order, page_prompt
from .variants import VARIANTS

ROOT = Path(__file__).resolve().parent.parent


def load_cfg(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def selected_models(cfg: dict, only: list[str] | None) -> list[str]:
    ids = [m["id"] for m in cfg["models"]]
    if only:
        unknown = set(only) - set(ids)
        if unknown:
            raise SystemExit(f"not in config: {sorted(unknown)}")
        ids = [i for i in ids if i in only]
    return ids


def cmd_check(cfg: dict, args) -> None:
    available = {m["id"]: m for m in asyncio.run(list_models())}
    for m in cfg["models"]:
        info = available.get(m["id"])
        if info is None:
            print(f"MISSING  {m['id']}")
            continue
        p = info["pricing"]
        params = info.get("supported_parameters") or []
        print(f"ok       {m['id']:<36} in ${float(p['prompt']) * 1e6:6.2f}/M  out ${float(p['completion']) * 1e6:6.2f}/M  "
              f"temperature={'temperature' in params} reasoning={'reasoning' in params}")


def _approx_tokens(s: str) -> int:
    return len(s) // 4 + 1


def cmd_estimate(cfg: dict, args) -> None:
    """Rough cost estimate: context grows with every page of the conversation."""
    available = {m["id"]: m for m in asyncio.run(list_models())}
    order = item_order(random.Random(0))
    answer_tokens = 40 + args.reasoning_tokens
    ctx, tin, tout = _approx_tokens(VARIANTS["base"].system_prompt), 0, 0
    for i, iid in enumerate(order):
        ctx += _approx_tokens(page_prompt(get_item(iid), i == 0))
        tin += ctx
        tout += answer_tokens
        ctx += 40
    n = args.n or cfg["n_participants"]
    print(f"per participant: ~{tin} input, ~{tout} output tokens ({len(order)} pages); n={n}")
    total = 0.0
    for mid in selected_models(cfg, args.models):
        p = available.get(mid, {}).get("pricing")
        if not p:
            print(f"{mid:<36} not available")
            continue
        c = n * (tin * float(p["prompt"]) + tout * float(p["completion"]))
        total += c
        print(f"{mid:<36} ~${c:8.2f}")
    print(f"{'total':<36} ~${total:8.2f}  (excl. retries; caching may lower it)")


def raw_dir(args) -> Path:
    # base data lives directly in data/raw/, every other variant in data/raw/<variant>/
    d = Path(args.raw_dir)
    return d if args.variant == "base" else d / args.variant


def cmd_preview(cfg: dict, args) -> None:
    v = VARIANTS[args.variant]
    order = item_order(random.Random(args.seed), variant=v)
    print(f"[system]\n{v.system_prompt}\n")
    for i, iid in enumerate(order):
        print(f"[user, page {i + 1}: {iid}]\n{page_prompt(get_item(iid, v), i == 0)}\n")


def cmd_run(cfg: dict, args) -> None:
    from .run import run_model

    async def main() -> None:
        for mid in selected_models(cfg, args.models):
            await run_model(mid, cfg, raw_dir(args), n=args.n, variant=VARIANTS[args.variant])

    asyncio.run(main())


def cmd_analyze(cfg: dict, args) -> None:
    from .analysis import analyze

    fam = {m["id"]: m.get("family", "") for m in cfg["models"]}
    out = Path(args.out_dir) if args.variant == "base" else Path(args.out_dir) / args.variant
    analyze(raw_dir(args), out, fam, variant=VARIANTS[args.variant])
    print((out / "summary.md").read_text())


def main() -> None:
    ap = argparse.ArgumentParser(prog="ma_llm")
    ap.add_argument("--config", default=str(ROOT / "config" / "study.yaml"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="check model IDs and pricing on OpenRouter")
    e = sub.add_parser("estimate", help="rough cost estimate")
    e.add_argument("--n", type=int)
    e.add_argument("--models", nargs="*")
    e.add_argument("--reasoning-tokens", type=int, default=150, help="assumed reasoning tokens per answer")
    p = sub.add_parser("preview", help="print one participant's prompts")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--variant", choices=list(VARIANTS), default="base")
    r = sub.add_parser("run", help="collect data (resumable)")
    r.add_argument("--n", type=int, help="participants per model (default: config)")
    r.add_argument("--models", nargs="*", help="subset of model IDs")
    r.add_argument("--raw-dir", default=str(ROOT / "data" / "raw"))
    r.add_argument("--variant", choices=list(VARIANTS), default="base")
    a = sub.add_parser("analyze", help="compute effects and write results/")
    a.add_argument("--raw-dir", default=str(ROOT / "data" / "raw"))
    a.add_argument("--out-dir", default=str(ROOT / "results"))
    a.add_argument("--variant", choices=list(VARIANTS), default="base")
    args = ap.parse_args()
    cfg = load_cfg(Path(args.config))
    {"check": cmd_check, "estimate": cmd_estimate, "preview": cmd_preview,
     "run": cmd_run, "analyze": cmd_analyze}[args.cmd](cfg, args)


if __name__ == "__main__":
    main()
