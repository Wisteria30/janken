from __future__ import annotations

from typing import Literal

type Hand = Literal["グー", "チョキ", "パー"]
type JankenResult = Literal["ユーザーの勝ち", "ユーザーの負け", "あいこ"]

HANDS: tuple[Hand, ...] = ("グー", "チョキ", "パー")

_WINNING_HANDS: dict[Hand, Hand] = {
    "グー": "チョキ",
    "チョキ": "パー",
    "パー": "グー",
}


def judge_janken(user_hand: Hand, system_hand: Hand) -> JankenResult:
    if user_hand == system_hand:
        return "あいこ"
    if _WINNING_HANDS[user_hand] == system_hand:
        return "ユーザーの勝ち"
    return "ユーザーの負け"
