"""Study variants used to probe *why* LLMs show mental-accounting effects.

base        Replication as in the paper (participant framing, Table 1 wording, within).
neutral     Same items, no survey/participant framing in the system prompt.
rational    Same items, model told to decide as a fully rational economic agent.
paraphrase  New stories and amounts with the same structure as each Table 1 item,
            to check whether effects depend on recognizing the textbook scenarios.
between     Original items, but each conversation sees only one condition per
            scenario (as in most original between-subjects studies).
"""

from __future__ import annotations

from dataclasses import dataclass

from .scenarios import BLOCKS, ITEMS, MRAB_OPTIONS, YES_NO_OPTIONS, Item

PARTICIPANT_PROMPT = (
    "You are taking part in an online survey about how people make decisions. "
    "Answer every question as a survey participant, according to your own judgement. "
    "There are no right or wrong answers. Always reply in exactly the requested format."
)
NEUTRAL_PROMPT = "Answer the following questions. Always reply in exactly the requested format."
RATIONAL_PROMPT = (
    "Answer the following questions as a fully rational economic decision-maker who "
    "treats money as fungible and ignores sunk costs and irrelevant framing. "
    "Always reply in exactly the requested format."
)

# Paraphrased items ----------------------------------------------------------------
# Same structure and predicted direction as the Table 1 item with the same id;
# different story, amounts and wording.

_GAME_Q = (
    "What price do you ask for the extra ticket if the buyer is a friend/is a stranger? "
    "And what price would you ask if the printed price had been $16 instead? "
    "If the buyer is a friend/stranger?"
)
_GAME_INTRO = (
    "You have tickets for a sold-out concert of a band you love, and one ticket is left "
    "over. "
)
_GAME_OUTRO = (
    " You want to sell the spare ticket, and you know that its printed price is $8. Someone "
    "would like to buy it. Reselling above the printed price is legal.\n" + _GAME_Q
)
_GYM_STATEMENTS = {
    "wasted_15": "I feel like I wasted $15",
    "wasted_nothing": "I feel like I wasted nothing, because the class was already paid for",
    "wasted_something": "I feel like I wasted something, but I cannot name a specific amount",
}
_GYM_Q = "How well does each of the following statements describe how you feel about the cost of the missed class?"
_PLANE_OPTIONS = [
    "Pay your friend $45 for the voucher",
    "Treat it as a gift and do not pay for the voucher",
    "Pay part of the price, but not the full amount, for example half",
]

PARAPHRASE_ITEMS: dict[str, Item] = {it.id: it for it in [
    Item("MrAB1", "MrAB",
         "Person A received two bonuses at work this month: one of $60 and another of $30. "
         "Person B received a single bonus of $90 this month. Who is happier?",
         "choice", MRAB_OPTIONS),
    Item("MrAB2", "MrAB",
         "Person A got a parking ticket for $80 and, later the same week, a second parking "
         "ticket for $40. Person B got one parking ticket for $120. Nothing else came of it. "
         "Who is more upset?",
         "choice", MRAB_OPTIONS),
    Item("MrAB3", "MrAB",
         "Person A received a $150 gift card for their birthday. The same week, they "
         "dropped their phone and paid $120 to repair the screen. Person B received a $30 "
         "gift card for their birthday. Who is happier?",
         "choice", MRAB_OPTIONS),
    Item("MrAB4", "MrAB",
         "Person A's washing machine broke and the repair cost $300. The same week, they "
         "found $30 in the pocket of an old coat. Person B's washing machine broke and the "
         "repair cost $270. Who is more upset?",
         "choice", MRAB_OPTIONS),
    Item("Game1", "Game",
         _GAME_INTRO + "A friend gave you this ticket for free; its printed price is $8."
         + _GAME_OUTRO, "game_prices", params={"face": 8, "alt": 16, "alt_label": "printed price"}),
    Item("Game2", "Game",
         _GAME_INTRO + "You bought it at the box office for its printed price of $8."
         + _GAME_OUTRO, "game_prices", params={"face": 8, "alt": 16, "alt_label": "printed price"}),
    Item("Game3", "Game",
         _GAME_INTRO + "Its printed price is $8, but you paid $16 for it to a reseller."
         + _GAME_OUTRO, "game_prices", params={"face": 8, "alt": 16, "alt_label": "printed price"}),
    Item("Drink1", "Drink",
         "It is a hot afternoon in the park and you would love an iced coffee. A friend "
         "offers to fetch one from the café of an upscale hotel nearby. They ask for the "
         "most you are willing to pay: they will only buy it if it costs that much or less. "
         "You trust your friend, and the price cannot be negotiated.\n"
         "What maximum price do you tell them?", "price"),
    Item("Drink2", "Drink",
         "It is a hot afternoon in the park and you would love an iced coffee. A friend "
         "offers to fetch one from a small, shabby kiosk nearby. They ask for the most you "
         "are willing to pay: they will only buy it if it costs that much or less. You "
         "trust your friend, and the price cannot be negotiated.\n"
         "What maximum price do you tell them?", "price"),
    Item("Jacket1", "Jacket",
         "You are about to buy a winter coat for $180 and a pair of headphones for $20. "
         "The cashier tells you that the headphones are on sale for $13 at another branch "
         "of the store, a 25-minute walk away.\nWould you go to the other branch?",
         "choice", YES_NO_OPTIONS),
    Item("Jacket2", "Jacket",
         "You are about to buy a winter coat for $20 and a pair of headphones for $180. "
         "The cashier tells you that the headphones are on sale for $173 at another branch "
         "of the store, a 25-minute walk away.\nWould you go to the other branch?",
         "choice", YES_NO_OPTIONS),
    Item("Play1", "Play",
         "You are going to a football match and already bought your ticket for $60. At the "
         "stadium gate you notice that the ticket is gone.\n"
         "Would you buy another ticket for $60?", "choice", YES_NO_OPTIONS),
    Item("Play2", "Play",
         "You are going to a football match and plan to buy a $60 ticket at the gate. At "
         "the stadium you notice that $60 in cash has fallen out of your pocket.\n"
         "Would you still buy a ticket for $60?", "choice", YES_NO_OPTIONS),
    Item("Gym1", "Gym",
         "You attend a yoga class every Thursday evening, the only time your job allows. "
         "The studio charges $15 per class, paid in advance and non-refundable. One "
         "Thursday, right after paying and changing, you get an urgent call and have to "
         "leave before the class starts.\n" + _GYM_Q,
         "ratings", params={"statements": _GYM_STATEMENTS}),
    Item("Gym2", "Gym",
         "You attend a yoga class every Thursday evening, the only time your job allows. "
         "You have an annual membership for $750 (roughly $15 per class). One Thursday, "
         "right after arriving and changing, you get an urgent call and have to leave "
         "before the class starts.\n" + _GYM_Q,
         "ratings", params={"statements": _GYM_STATEMENTS}),
    Item("Plane1", "Plane",
         "You are on a long train journey with a friend who has upgraded to first class. "
         "They have two upgrade vouchers worth $45 each: they bought one at the regular "
         "price of $45 and got the other one for free. Only one voucher is needed for an "
         "upgrade, and your friend offers you the voucher they bought so you can upgrade "
         "too.\nWhat do you think is the most appropriate thing to do?",
         "choice", _PLANE_OPTIONS),
    Item("Plane2", "Plane",
         "You are on a long train journey with a friend who has upgraded to first class. "
         "They have two upgrade vouchers worth $45 each: they bought one at the regular "
         "price of $45 and got the other one for free. Only one voucher is needed for an "
         "upgrade, and your friend offers you the voucher they got for free so you can "
         "upgrade too.\nWhat do you think is the most appropriate thing to do?",
         "choice", _PLANE_OPTIONS),
]}

# Between-subjects: all four MrAB items (each is a self-contained comparison), one
# Game condition and one condition of every two-condition scenario.
BETWEEN_GROUPS: list[list[str]] = [
    ["MrAB1"], ["MrAB2"], ["MrAB3"], ["MrAB4"],
    ["Game1", "Game2", "Game3"],
    ["Drink1", "Drink2"], ["Jacket1", "Jacket2"], ["Play1", "Play2"],
    ["Gym1", "Gym2"], ["Plane1", "Plane2"],
]


@dataclass(frozen=True)
class Variant:
    name: str
    system_prompt: str
    items: dict[str, Item]
    design: str = "within"  # "within" | "between"
    blocks: tuple = tuple(tuple(b) for b in BLOCKS)


VARIANTS: dict[str, Variant] = {
    "base": Variant("base", PARTICIPANT_PROMPT, ITEMS),
    "neutral": Variant("neutral", NEUTRAL_PROMPT, ITEMS),
    "rational": Variant("rational", RATIONAL_PROMPT, ITEMS),
    "paraphrase": Variant("paraphrase", PARTICIPANT_PROMPT, PARAPHRASE_ITEMS),
    "between": Variant("between", PARTICIPANT_PROMPT, ITEMS, design="between"),
}
