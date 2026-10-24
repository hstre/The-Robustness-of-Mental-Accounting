"""Survey flow, prompt construction and answer parsing.

One simulated participant = one independent multi-turn conversation. Each survey
page (item) is one user turn; the model's previous answers stay in the context,
as they would in a human's memory of earlier pages of a within-subjects survey.
"""

from __future__ import annotations

import json
import random
import re
from typing import Any

from .scenarios import FIN_LIT, GYM_SCALE, QUALITY, Item
from .variants import BETWEEN_GROUPS, PARTICIPANT_PROMPT, VARIANTS, Variant

SYSTEM_PROMPT = PARTICIPANT_PROMPT

INTRO = (
    "Welcome to this study on decision-making. On the following pages you will read short "
    "everyday scenarios and answer a question about each one. Please read every scenario "
    "carefully and answer honestly.\n\n"
)


def item_order(rng: random.Random, include_extras: bool = True, variant: Variant | None = None) -> list[str]:
    """Within: randomized block order (fixed order within blocks), as in the paper.
    Between: one random condition per scenario, all in random order.
    Followed by the financial-literacy items and the data-quality question."""
    variant = variant or VARIANTS["base"]
    if variant.design == "between":
        order = [rng.choice(g) for g in BETWEEN_GROUPS]
        rng.shuffle(order)
    else:
        blocks = [list(b) for b in variant.blocks]
        rng.shuffle(blocks)
        order = [i for b in blocks for i in b]
    if include_extras:
        order += [it.id for it in FIN_LIT] + [QUALITY.id]
    return order


def get_item(item_id: str, variant: Variant | None = None) -> Item:
    items = (variant or VARIANTS["base"]).items
    if item_id in items:
        return items[item_id]
    for it in FIN_LIT:
        if it.id == item_id:
            return it
    if item_id == QUALITY.id:
        return QUALITY
    raise KeyError(item_id)


def game_keys(item: Item) -> list[str]:
    alt = item.params["alt"]
    return ["friend", "stranger", f"friend_face{alt}", f"stranger_face{alt}"]


def format_instruction(item: Item, options: list[str] | None = None) -> str:
    options = options if options is not None else item.options
    if item.kind == "choice":
        opts = "\n".join(f"- {o}" for o in options)
        return (
            f"Options:\n{opts}\n\n"
            'Reply only with a JSON object of the form {"answer": "<one option, copied exactly>"}.'
        )
    if item.kind == "price":
        return 'Reply only with a JSON object of the form {"price": <amount in US dollars, a number>}.'
    if item.kind == "game_prices":
        alt, label = item.params["alt"], item.params.get("alt_label", "face value")
        k = game_keys(item)
        return (
            "Reply only with a JSON object with four prices in US dollars (numbers):\n"
            f'{{"{k[0]}": <price if the buyer is a friend>, '
            f'"{k[1]}": <price if the buyer is a stranger>, '
            f'"{k[2]}": <price for a friend if the {label} were ${alt}>, '
            f'"{k[3]}": <price for a stranger if the {label} were ${alt}>}}'
        )
    if item.kind == "ratings":
        st = item.params["statements"]
        stmts = "\n".join(f'- "{k}": {v}' for k, v in st.items())
        form = ", ".join(f'"{k}": <1-5>' for k in st)
        return (
            f"Rate each statement on a scale from 1 to 5 ({GYM_SCALE}).\n{stmts}\n\n"
            f"Reply only with a JSON object of the form {{{form}}}."
        )
    raise ValueError(item.kind)


def page_prompt(item: Item, first: bool, options: list[str] | None = None) -> str:
    return (INTRO if first else "") + item.text + "\n\n" + format_instruction(item, options)


RETRY_PROMPT = (
    "Your answer could not be read. Please answer the same question again and reply only "
    "with the JSON object in the requested format, without any other text."
)

# Parsing -----------------------------------------------------------------------

_JSON_RE = re.compile(r"\{.*?\}", re.DOTALL)
_NUM_RE = re.compile(r"-?\d+(?:[.,]\d+)?")


def _extract_json(text: str) -> dict[str, Any] | None:
    if not text:
        return None
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    for m in _JSON_RE.finditer(text):
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def _to_number(v: Any) -> float | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = _NUM_RE.search(v.replace("$", ""))
        if m:
            return float(m.group(0).replace(",", "."))
    return None


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9$]+", " ", s.lower()).strip()


def _match_option(answer: Any, options: list[str]) -> str | None:
    if not isinstance(answer, str):
        if isinstance(answer, (int, float)) and options == QUALITY.options:
            answer = str(int(answer))
        else:
            return None
    a = _norm(answer)
    exact = [o for o in options if _norm(o) == a]
    if exact:
        return exact[0]
    # Quality scale: accept "4", "5 - absolutely serious", etc.
    if options == QUALITY.options:
        m = re.match(r"\s*([1-5])", answer)
        return options[int(m.group(1)) - 1] if m else None
    # Unique prefix match (e.g. "Pay your friend $35"), then unique containment.
    # Only for long options/answers, so "Both ..." never matches option "B".
    pref = [o for o in options if len(_norm(o)) >= 4 and len(a) >= 4
            and (_norm(o).startswith(a) or a.startswith(_norm(o)))]
    if len(pref) == 1:
        return pref[0]
    cont = [o for o in options if re.search(rf"(^| ){re.escape(_norm(o))}( |$)", a)]
    if len(cont) == 1:
        return cont[0]
    return None


def parse_answer(item: Item, text: str, options: list[str] | None = None) -> dict[str, Any] | None:
    """Return the parsed answer dict or None if the reply is unusable."""
    options = options if options is not None else item.options
    obj = _extract_json(text)
    if obj is None:
        return None
    if item.kind == "choice":
        opt = _match_option(obj.get("answer"), options)
        return {"answer": opt} if opt is not None else None
    if item.kind == "price":
        p = _to_number(obj.get("price"))
        return {"price": p} if p is not None and p >= 0 else None
    if item.kind == "game_prices":
        out = {}
        for k in game_keys(item):
            p = _to_number(obj.get(k))
            if p is None or p < 0:
                return None
            out[k] = p
        return out
    if item.kind == "ratings":
        out = {}
        for k in item.params["statements"]:
            r = _to_number(obj.get(k))
            if r is None or r not in (1, 2, 3, 4, 5):
                return None
            out[k] = int(r)
        return out
    raise ValueError(item.kind)
