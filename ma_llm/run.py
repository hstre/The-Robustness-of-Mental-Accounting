"""Run simulated participants against OpenRouter models and store raw transcripts."""

from __future__ import annotations

import asyncio
import hashlib
import json
import random
import time
from pathlib import Path
from typing import Any

from .client import OpenRouterClient, OpenRouterError
from .survey import RETRY_PROMPT, SYSTEM_PROMPT, get_item, item_order, page_prompt, parse_answer


def model_slug(model_id: str) -> str:
    return model_id.replace("/", "__").replace(":", "_")


def participant_seed(model_id: str, pid: int) -> int:
    return int(hashlib.sha256(f"{model_id}|{pid}".encode()).hexdigest()[:12], 16)


def done_ids(path: Path) -> set[int]:
    if not path.exists():
        return set()
    ids = set()
    for line in path.read_text().splitlines():
        if line.strip():
            ids.add(json.loads(line)["participant_id"])
    return ids


async def run_participant(
    client: OpenRouterClient, model_id: str, pid: int, cfg: dict[str, Any]
) -> dict[str, Any]:
    rng = random.Random(participant_seed(model_id, pid))
    order = item_order(rng)
    gen = cfg["generation"]
    params = {
        "temperature": gen.get("temperature"),
        "max_tokens": gen.get("max_tokens"),
        "reasoning": gen.get("reasoning"),
    }
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    pages, answers = [], {}
    cost, tokens_in, tokens_out = 0.0, 0, 0
    rec: dict[str, Any] = {
        "participant_id": pid, "model": model_id, "order": order,
        "started": time.time(), "complete": False, "error": None,
    }
    try:
        for idx, item_id in enumerate(order):
            item = get_item(item_id)
            options = list(item.options)
            if cfg.get("shuffle_options") and item.kind == "choice" and item.scenario != "Quality":
                rng.shuffle(options)
            messages.append({"role": "user", "content": page_prompt(item, idx == 0, options)})
            raw, parsed = [], None
            for attempt in range(cfg.get("max_parse_retries", 2) + 1):
                resp = await client.chat(model_id, messages, **params)
                u = resp["usage"] or {}
                cost += float(u.get("cost") or 0)
                tokens_in += int(u.get("prompt_tokens") or 0)
                tokens_out += int(u.get("completion_tokens") or 0)
                raw.append({"content": resp["content"], "finish_reason": resp["finish_reason"],
                            "provider": resp["provider"]})
                messages.append({"role": "assistant", "content": resp["content"]})
                parsed = parse_answer(item, resp["content"], options)
                if parsed is not None:
                    break
                messages.append({"role": "user", "content": RETRY_PROMPT})
            pages.append({"item": item_id, "position": idx, "options": options,
                          "raw": raw, "parsed": parsed})
            if parsed is None:
                truncated = all(r["finish_reason"] == "length" for r in raw)
                rec["error"] = f"{'truncated' if truncated else 'unparseable'} answer on {item_id}"
                break
            answers[item_id] = parsed
        else:
            rec["complete"] = True
    except OpenRouterError as e:
        rec["error"] = str(e)
    rec.update(answers=answers, pages=pages, cost_usd=cost,
               prompt_tokens=tokens_in, completion_tokens=tokens_out, finished=time.time())
    return rec


async def run_model(model_id: str, cfg: dict[str, Any], out_dir: Path, n: int | None = None) -> None:
    n = n or cfg["n_participants"]
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{model_slug(model_id)}.jsonl"
    todo = [pid for pid in range(n) if pid not in done_ids(path)]
    if not todo:
        print(f"[{model_id}] already complete ({n})")
        return
    client = OpenRouterClient()
    sem = asyncio.Semaphore(cfg.get("concurrency", 8))
    lock = asyncio.Lock()
    stats = {"done": 0, "complete": 0, "cost": 0.0}

    async def one(pid: int) -> None:
        async with sem:
            rec = await run_participant(client, model_id, pid, cfg)
        async with lock:
            if rec["error"] and " answer on " not in rec["error"]:
                # API/transport failure: not a participant outcome; retried on the next run.
                print(f"[{model_id}] pid {pid} not saved: {rec['error'][:200]}")
                return
            with path.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            stats["done"] += 1
            stats["complete"] += rec["complete"]
            stats["cost"] += rec["cost_usd"]
            if stats["done"] % 10 == 0 or stats["done"] == len(todo):
                print(f"[{model_id}] {stats['done']}/{len(todo)} done, "
                      f"{stats['complete']} complete, ${stats['cost']:.2f}")

    try:
        await asyncio.gather(*(one(pid) for pid in todo))
    finally:
        await client.close()
