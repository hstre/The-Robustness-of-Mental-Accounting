"""Survey material from Priolo et al. (2026), "The Robustness of Mental Accounting
Across 21 Countries", Journal of Consumer Research, Table 1.

Scenario texts are taken verbatim from Table 1 (English/US-dollar version). The
paper's per-country adapted monetary values and the exact financial-literacy items
are only published on OSF (https://osf.io/kgesy) and are not reproduced here; see
README.md ("Abweichungen") for what that means.

Every item has an ``id``, a ``scenario`` (the effect it belongs to), the question
``text`` and an answer ``kind`` that determines the JSON schema the model must use.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Response options -----------------------------------------------------------

MRAB_OPTIONS = ["A", "B", "No difference"]

PLANE_OPTIONS = [
    "Pay your friend $35 for the coupon",
    "Consider it a gift and do not pay for the coupon",
    "Pay some, but not the full amount for the coupon, for example, half the price",
]

YES_NO_OPTIONS = ["Yes", "No"]

GYM_STATEMENTS = {
    "wasted_20": "I feel like I wasted $20",
    "wasted_nothing": "I feel like I wasted nothing, since my visit had already been paid for",
    "wasted_something": "I feel like I wasted something, but no specific amount or measure comes to mind",
}
GYM_SCALE = "1 = Strongly agree, 2 = Agree, 3 = Neither agree nor disagree, 4 = Disagree, 5 = Strongly disagree"


@dataclass(frozen=True)
class Item:
    id: str
    scenario: str
    text: str
    kind: str  # "choice" | "price" | "game_prices" | "ratings"
    options: list[str] = field(default_factory=list)
    # game_prices: {"face": market value, "alt": hypothetical face value}
    # ratings: {"statements": {key: text}}, first key = "I wasted <amount>"
    params: dict = field(default_factory=dict)


# Combined outcomes: MrAB (Thaler 1985) -- DV: A / B / No difference ----------

MRAB1 = Item(
    "MrAB1", "MrAB",
    "Person A was given two tickets to the lottery. They won $50 with one ticket and $25 "
    "with the other ticket. Person B was given a ticket to one lottery. They won $75. "
    "Who is happier?",
    "choice", MRAB_OPTIONS,
)
MRAB2 = Item(
    "MrAB2", "MrAB",
    "Person A received a fine and owed $100. The same day, they received a second fine and "
    "owed $50. Person B received a fine and owed $150. There were no other repercussions "
    "from this mistake. Who is more upset?",
    "choice", MRAB_OPTIONS,
)
MRAB3 = Item(
    "MrAB3", "MrAB",
    "Person A bought a lottery ticket and won $100. Also, they damaged one door in their "
    "apartment in an accident and had to pay the landlord $80. Person B bought a lottery "
    "ticket and won $20. Who is happier?",
    "choice", MRAB_OPTIONS,
)
MRAB4 = Item(
    "MrAB4", "MrAB",
    "Person A damaged their car in a parking lot. They had to spend $200 to repair the "
    "damage. The same day they damaged the car, they won $25 in a raffle. Person B damaged "
    "their car in a parking lot. They had to spend $175 to repair the damage. "
    "Who is more upset?",
    "choice", MRAB_OPTIONS,
)

# Transaction utility: Game (Thaler 1985) -- DV: willingness to accept --------

_GAME_QUESTION = (
    "What price do you ask for selling the extra ticket if the person you sell it to is a "
    "friend/is a stranger? What price would you have asked for if you found out that the "
    "ticket's face value price was $10 instead? If they are a friend/stranger?"
)

GAME1 = Item(
    "Game1", "Game",
    "You are going to a sold-out game of your favorite local sports team, and you have an "
    "extra ticket. The price marked on the ticket is $5, but this ticket has been offered to "
    "you by a friend for free. You want to get rid of the extra ticket, and you know the "
    "ticket's face value price is $5. You find someone who wants the ticket. There is no law "
    "against charging more than the price marked on the ticket.\n" + _GAME_QUESTION,
    "game_prices", params={"face": 5, "alt": 10},
)
GAME2 = Item(
    "Game2", "Game",
    "You are going to a sold-out game of your favorite local sports team, and you have an "
    "extra ticket. The price marked on the ticket is $5, which is what you paid for each "
    "ticket. You want to get rid of the extra ticket, and you know the ticket's face value "
    "price is $5. You find someone who wants the ticket. There is no law against charging "
    "more than the price marked on the ticket.\n" + _GAME_QUESTION,
    "game_prices", params={"face": 5, "alt": 10},
)
GAME3 = Item(
    "Game3", "Game",
    "You are going to a sold-out game of your favorite local sports team, and you have an "
    "extra ticket. The ticket's face value price is $5, but you paid $10 for each ticket when "
    "you bought them from another person. You want to get rid of the extra ticket and you "
    "know the ticket's face value price is $5. You find someone who wants the ticket. There "
    "is no law against charging more than the price marked on the ticket.\n" + _GAME_QUESTION,
    "game_prices", params={"face": 5, "alt": 10},
)

# Transaction utility: Drink (Thaler 1985) -- DV: willingness to pay ----------

DRINK1 = Item(
    "Drink1", "Drink",
    "You are on the beach on a hot day, and you would really like a cold drink. A friend "
    "offers to go buy the drink from a fancy resort hotel. They ask how much you are willing "
    "to pay for the drink: they will only buy it if it costs as much or less than the price "
    "you state. You trust your friend, and there is no possibility of bargaining with the "
    "bartender.\nWhat price do you tell them?",
    "price",
)
DRINK2 = Item(
    "Drink2", "Drink",
    "You are on the beach on a hot day and you would really like a cold drink. A friend "
    "offers to go buy the drink from a small, run-down grocery store. They ask how much you "
    "are willing to pay for the drink: they will only buy it if it costs as much or less "
    "than the price you state. You trust your friend, and there is no possibility of "
    "bargaining with the store owner.\nWhat price do you tell them?",
    "price",
)

# Outcome framing: Jacket (Kahneman & Tversky 1982; Tversky & Kahneman 1981) --

JACKET1 = Item(
    "Jacket1", "Jacket",
    "You are about to purchase a jacket for $125 and a Bluetooth speaker for $15. The "
    "salesman informs you that the speaker you wish to buy is on sale for $10 at the other "
    "branch store, located 20 minutes away.\nWould you make the trip to the other store?",
    "choice", YES_NO_OPTIONS,
)
JACKET2 = Item(
    "Jacket2", "Jacket",
    "You are about to purchase a jacket for $15 and a Bluetooth speaker for $125. The "
    "salesman informs you that the speaker you wish to buy is on sale for $120 at the other "
    "branch store, located 20 minutes away.\nWould you make the trip to the other store?",
    "choice", YES_NO_OPTIONS,
)

# Sunk cost: Play (Tversky & Kahneman 1981) -- DV: Yes/No ---------------------

PLAY1 = Item(
    "Play1", "Play",
    "Imagine that you are on your way to a music event with a ticket for which you have paid "
    "$40. On entering the venue, you discover that you have lost the ticket.\n"
    "Would you pay $40 for another ticket?",
    "choice", YES_NO_OPTIONS,
)
PLAY2 = Item(
    "Play2", "Play",
    "Imagine that you are on your way to a music event, and intend to buy a ticket worth "
    "$40. On entering the venue, you realize that you have lost $40 in cash.\n"
    "Would you still pay $40 for a ticket?",
    "choice", YES_NO_OPTIONS,
)

# Local vs global representations: Gym (Shafir & Thaler 2006) -----------------

_GYM_QUESTION = (
    "How well does each of the following statements capture your feelings about the cost "
    "of the missed workout?"
)

GYM1 = Item(
    "Gym1", "Gym",
    "Imagine that you go to the gym on a regular basis. Due to your busy working schedule, "
    "you can only go on Monday nights. The membership to the gym allows you to pay $20 "
    "(non-refundable) per session. One Monday, just after you have paid and changed into "
    "your gym clothes, you receive a phone call that requires you to leave and forgo your "
    "exercise that evening.\n" + _GYM_QUESTION,
    "ratings", params={"statements": GYM_STATEMENTS},
)
GYM2 = Item(
    "Gym2", "Gym",
    "Imagine that you go to the gym on a regular basis. Due to your busy working schedule, "
    "you can only go on Monday nights. The membership to the gym costs you $1000 a year "
    "(i.e., roughly $20 per visit). One Monday, just after you have paid and changed into "
    "your gym clothes, you receive a phone call that requires you to leave and forgo your "
    "exercise that evening.\n" + _GYM_QUESTION,
    "ratings", params={"statements": GYM_STATEMENTS},
)

# Purchases and bonuses: Plane (Shafir & Thaler 2006) -------------------------

_PLANE_QUESTION = "What do you think is the most appropriate thing to do?"

PLANE1 = Item(
    "Plane1", "Plane",
    "You are flying with a friend who has upgraded their ticket to business class and has "
    "two coupons, each worth $35, which can be used to upgrade your ticket from economy to "
    "business class. They purchased one coupon for the standard price of $35 and received "
    "the other one for free. Just one coupon is required to upgrade your class on the "
    "current flight, and your friend offers you the coupon that they purchased so that you "
    "can upgrade as well.\n" + _PLANE_QUESTION,
    "choice", PLANE_OPTIONS,
)
PLANE2 = Item(
    "Plane2", "Plane",
    "You are flying with a friend who has upgraded their ticket to business class and has "
    "two coupons, each worth $35, which could be used to upgrade your ticket from economy "
    "to business class. They purchased one coupon for the standard price of $35 and "
    "received the other one for free. Just one coupon is required to upgrade your class on "
    "the current flight and your friend offers you the coupon that they got for free so "
    "that you can upgrade your ticket as well.\n" + _PLANE_QUESTION,
    "choice", PLANE_OPTIONS,
)

ITEMS: dict[str, Item] = {
    it.id: it
    for it in [
        MRAB1, MRAB2, MRAB3, MRAB4,
        GAME1, GAME2, GAME3,
        DRINK1, DRINK2,
        JACKET1, JACKET2,
        PLAY1, PLAY2,
        GYM1, GYM2,
        PLANE1, PLANE2,
    ]
}

# Block design ----------------------------------------------------------------
# The paper used "three blocks with four scenarios each and one with five
# scenarios", block order randomized, fixed order within a block, and conditions
# of the same scenario always in different blocks. The exact assignment is on OSF;
# this is a reconstruction that satisfies all stated constraints (17 items,
# block sizes 5/4/4/4, no scenario twice within a block).
BLOCKS: list[list[str]] = [
    ["MrAB1", "Game1", "Drink1", "Jacket1", "Gym1"],
    ["MrAB2", "Game2", "Play1", "Plane1"],
    ["MrAB3", "Game3", "Drink2", "Gym2"],
    ["MrAB4", "Jacket2", "Play2", "Plane2"],
]

# Financial literacy (exploratory) --------------------------------------------
# Four items in the spirit of Lusardi & Mitchell (2014), Skagerlund et al. (2018)
# and van Rooij, Lusardi & Alessie (2012). The paper's exact wording is on OSF.
FIN_LIT = [
    Item(
        "FL_interest", "FinLit",
        "Suppose you had $100 in a savings account and the interest rate was 2% per year. "
        "After 5 years, how much do you think you would have in the account if you left "
        "the money to grow?",
        "choice", ["More than $102", "Exactly $102", "Less than $102", "Do not know"],
    ),
    Item(
        "FL_inflation", "FinLit",
        "Imagine that the interest rate on your savings account was 1% per year and "
        "inflation was 2% per year. After 1 year, how much would you be able to buy with "
        "the money in this account?",
        "choice", ["More than today", "Exactly the same", "Less than today", "Do not know"],
    ),
    Item(
        "FL_compound", "FinLit",
        "Suppose you had $100 in a savings account and the interest rate is 20% per year "
        "and you never withdraw money or interest payments. After 5 years, how much would "
        "you have on this account in total?",
        "choice", ["More than $200", "Exactly $200", "Less than $200", "Do not know"],
    ),
    Item(
        "FL_risk", "FinLit",
        "Please tell me whether this statement is true or false: Buying a single company's "
        "stock usually provides a safer return than a stock mutual fund.",
        "choice", ["True", "False", "Do not know"],
    ),
]
FIN_LIT_CORRECT = {
    "FL_interest": "More than $102",
    "FL_inflation": "Less than today",
    "FL_compound": "More than $200",
    "FL_risk": "False",
}

QUALITY = Item(
    "Quality", "Quality",
    "How serious have you been about filling in the survey?",
    "choice",
    ["1 - Not serious at all", "2", "3", "4", "5 - Absolutely serious"],
)
