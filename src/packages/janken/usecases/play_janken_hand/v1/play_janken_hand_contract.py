"""既存のじゃんけんセッションにユーザーの手を適用し、システムの手と勝敗を返す。"""

from __future__ import annotations

from typing import ClassVar, Literal, Protocol

from pydantic import Field
from usecaseapi import (
    Contract,
    Model,
    UseCase,
    UseCaseError,
    UseCaseRef,
    define_usecase,
)


class PlayJankenHandUseCaseInput(Model):
    """じゃんけんセッションを 1 手進めるための入力を表す。"""

    session_id: str = Field(description="対象のじゃんけんセッションを識別する値。")
    user_hand: Literal["グー", "チョキ", "パー"] = Field(
        description="ユーザーが出すじゃんけんの手。"
    )


class PlayJankenHandUseCaseOutput(Model):
    """じゃんけん 1 手分のシステム入力、勝敗、次状態を表す。"""

    session_id: str = Field(description="対象のじゃんけんセッションを識別する値。")
    user_hand: Literal["グー", "チョキ", "パー"] = Field(
        description="判定に使用されたユーザーの手。"
    )
    system_hand: Literal["グー", "チョキ", "パー"] = Field(
        description="判定に使用されたシステムの手。"
    )
    result: Literal["ユーザーの勝ち", "ユーザーの負け", "あいこ"] = Field(
        description="じゃんけん 1 手分の勝敗。"
    )
    status: Literal["waiting_for_user_hand", "finished"] = Field(
        description="あいこなら継続、勝敗確定なら終了を示す状態。"
    )
    message: str = Field(description="CLI または HTTP で利用する利用者向けメッセージ。")


class JankenSessionError(UseCaseError):
    code: ClassVar[str] = "packages.janken.play_janken_hand.session_error"


class InvalidJankenHandError(JankenSessionError):
    code: ClassVar[str] = "packages.janken.play_janken_hand.invalid_hand"


class JankenSessionNotFoundError(JankenSessionError):
    code: ClassVar[str] = "packages.janken.play_janken_hand.session_not_found"


class JankenSessionAlreadyFinishedError(JankenSessionError):
    code: ClassVar[str] = "packages.janken.play_janken_hand.session_already_finished"


class PlayJankenHand(UseCase[PlayJankenHandUseCaseInput, PlayJankenHandUseCaseOutput], Protocol):
    """既存のじゃんけんセッションにユーザーの手を適用し、システムの手と勝敗を返す。"""

    async def __call__(
        self, input: PlayJankenHandUseCaseInput, /
    ) -> PlayJankenHandUseCaseOutput: ...


PLAY_JANKEN_HAND_USECASE: UseCaseRef[PlayJankenHandUseCaseInput, PlayJankenHandUseCaseOutput] = (
    define_usecase(
        PlayJankenHand,
        Contract(
            name="packages.janken.play_janken_hand",
            version=1,
            input=PlayJankenHandUseCaseInput,
            output=PlayJankenHandUseCaseOutput,
            raises=(JankenSessionError,),
            known_errors=(
                InvalidJankenHandError,
                JankenSessionNotFoundError,
                JankenSessionAlreadyFinishedError,
            ),
            stable=True,
            deprecated=False,
            description="既存のじゃんけんセッションにユーザーの手を適用し、システムの手と勝敗を返す。",
            tags=("janken", "game-step"),
        ),
    )
)
