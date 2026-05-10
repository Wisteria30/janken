from __future__ import annotations

from typing import Literal

type Direction = Literal["上", "下", "右", "左"]
type Initiative = Literal["user", "system"]
type FinalResult = Literal["ユーザーの勝ち", "ユーザーの負け"]

DIRECTIONS: tuple[Direction, ...] = ("上", "下", "右", "左")


def judge_direction(
    initiative: Initiative,
    user_direction: Direction,
    system_direction: Direction,
) -> FinalResult | None:
    if user_direction != system_direction:
        return None
    if initiative == "user":
        return "ユーザーの勝ち"
    return "ユーザーの負け"
