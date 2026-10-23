import asyncio
import json
import random

import numpy as np

from ma_llm import analysis
from ma_llm.run import run_participant
from ma_llm.scenarios import FIN_LIT, ITEMS, PLANE_OPTIONS, QUALITY
from ma_llm.survey import get_item, parse_answer

CFG = {"generation": {"temperature": 1.0, "max_tokens": 100, "reasoning": None},
       "max_parse_retries": 2, "shuffle_options": False}


def test_parse_variants():
    mrab = ITEMS["MrAB1"]
    assert parse_answer(mrab, '```json\n{"answer": "A"}\n```') == {"answer": "A"}
    assert parse_answer(mrab, '{"answer": "Person B"}') == {"answer": "B"}
    assert parse_answer(mrab, '{"answer": "no difference"}') == {"answer": "No difference"}
    assert parse_answer(mrab, '{"answer": "Both are equally happy"}') is None
    assert parse_answer(mrab, "As an AI, I don't have feelings.") is None
    plane = ITEMS["Plane1"]
    assert parse_answer(plane, '{"answer": "Pay your friend $35 for the coupon"}') == {"answer": PLANE_OPTIONS[0]}
    assert parse_answer(ITEMS["Drink1"], '{"price": "$4.50"}') == {"price": 4.5}
    assert parse_answer(ITEMS["Gym1"], '{"wasted_20": 2, "wasted_nothing": 4, "wasted_something": 3}')["wasted_20"] == 2
    assert parse_answer(ITEMS["Gym1"], '{"wasted_20": 7, "wasted_nothing": 4, "wasted_something": 3}') is None
    assert parse_answer(QUALITY, '{"answer": "5"}') == {"answer": QUALITY.options[4]}


def _human_like(item_id: str, rng: random.Random) -> str:
    """Synthetic respondent that shows the classic effects with noise."""
    it = get_item(item_id)
    if item_id.startswith("MrAB"):
        pred = {"MrAB1": "A", "MrAB2": "A", "MrAB3": "B", "MrAB4": "B"}[item_id]
        a = pred if rng.random() < 0.6 else rng.choice(it.options)
        return json.dumps({"answer": a})
    if item_id.startswith("Game"):
        f = lambda base: base * rng.choice([0, 0.8, 1, 1])
        s = lambda base: base * rng.choice([1, 1, 1.5, 2])
        return json.dumps({"friend": f(5), "stranger": s(5), "friend_face10": f(10), "stranger_face10": s(10)})
    if item_id == "Drink1":
        return json.dumps({"price": round(rng.lognormvariate(1.6, 0.4), 2)})
    if item_id == "Drink2":
        return json.dumps({"price": round(rng.lognormvariate(1.0, 0.4), 2)})
    if item_id in ("Jacket1", "Play2"):
        return json.dumps({"answer": "Yes" if rng.random() < 0.7 else "No"})
    if item_id in ("Jacket2", "Play1"):
        return json.dumps({"answer": "Yes" if rng.random() < 0.4 else "No"})
    if item_id.startswith("Gym"):
        base = 2 if item_id == "Gym1" else 3
        r = lambda: min(5, max(1, base + rng.choice([-1, 0, 0, 1])))
        return json.dumps({"wasted_20": r(), "wasted_nothing": r(), "wasted_something": r()})
    if item_id == "Plane1":
        return json.dumps({"answer": PLANE_OPTIONS[0] if rng.random() < 0.6 else PLANE_OPTIONS[1]})
    if item_id == "Plane2":
        return json.dumps({"answer": PLANE_OPTIONS[0] if rng.random() < 0.2 else PLANE_OPTIONS[1]})
    if item_id == "Quality":
        return "Sure! " + json.dumps({"answer": "5 - Absolutely serious"})
    return json.dumps({"answer": it.options[0]})


class FakeClient:
    """Answers the last page in the conversation; fails the first try of Drink2 once."""

    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        self.failed_once = False

    async def chat(self, model, messages, **params):
        last = next(m["content"] for m in reversed(messages) if m["role"] == "user")
        if last.startswith("Your answer could not be read"):
            last = [m["content"] for m in messages if m["role"] == "user"][-2]
        item_id = next(i for i in [*ITEMS, *(f.id for f in FIN_LIT), "Quality"]
                       if get_item(i).text in last)
        if item_id == "Drink2" and not self.failed_once:
            self.failed_once = True
            return {"content": "I'd say about three dollars.", "reasoning": None,
                    "usage": {"cost": 0.001}, "provider": "x", "finish_reason": "stop"}
        return {"content": _human_like(item_id, self.rng), "reasoning": None,
                "usage": {"cost": 0.001, "prompt_tokens": 10, "completion_tokens": 5},
                "provider": "x", "finish_reason": "stop"}


def test_end_to_end(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    for model in ("fake/a", "fake/b", "fake/c", "fake/d"):
        with (raw / f"{model.replace('/', '__')}.jsonl").open("w") as f:
            for pid in range(120):
                rec = asyncio.run(run_participant(FakeClient(1000 * len(model) + pid + ord(model[-1])), model, pid, CFG))
                assert rec["complete"], rec["error"]
                f.write(json.dumps(rec) + "\n")
    out = tmp_path / "results"
    analysis.analyze(raw, out)
    eff = __import__("pandas").read_csv(out / "effects_by_model.csv")
    # every built-in effect should be detected in the synthetic data
    assert eff["replicated"].all(), eff[~eff["replicated"]]
    meta = __import__("pandas").read_csv(out / "meta.csv")
    assert (meta["estimate"] > 0).all()
    assert (out / "summary.md").exists()


def test_degenerate_model_is_finite():
    # A model that always answers the same way must not produce infinite log ORs.
    y1, y0 = np.ones(50, bool), np.zeros(50, bool)
    est, se = analysis.log_or_binary(y1, y0)
    assert np.isfinite(est) and np.isfinite(se) and est > 0
    est, se = analysis.evidence_ratio(0, 50)
    assert np.isfinite(est) and est < 0
