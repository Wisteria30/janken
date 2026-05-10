"""じゃんけん単体の新しいメモリ上セッションを開始する。"""

from __future__ import annotations

from typing import Literal, Protocol

from pydantic import Field
from usecaseapi import (
    Contract,
    Model,
    UseCase,
    UseCaseRef,
    define_usecase,
)


class StartJankenSessionUseCaseInput(Model):
    """じゃんけんセッション開始に必要な入力を表す。"""

    pass


class StartJankenSessionUseCaseOutput(Model):
    """開始されたじゃんけんセッションの識別子と初期状態を表す。"""

    session_id: str = Field(
        description="アプリケーション実行中のメモリ上でセッションを識別する値。"
    )
    status: Literal["waiting_for_user_hand"] = Field(
        description="じゃんけんの手入力待ちであることを示す状態。"
    )
    message: str = Field(description="CLI または HTTP で利用する利用者向けメッセージ。")


class StartJankenSession(
    UseCase[StartJankenSessionUseCaseInput, StartJankenSessionUseCaseOutput], Protocol
):
    """じゃんけん単体の新しいメモリ上セッションを開始する。"""

    async def __call__(
        self, input: StartJankenSessionUseCaseInput, /
    ) -> StartJankenSessionUseCaseOutput: ...


START_JANKEN_SESSION_USECASE: UseCaseRef[
    StartJankenSessionUseCaseInput, StartJankenSessionUseCaseOutput
] = define_usecase(
    StartJankenSession,
    Contract(
        name="packages.janken.start_janken_session",
        version=1,
        input=StartJankenSessionUseCaseInput,
        output=StartJankenSessionUseCaseOutput,
        raises=(),
        known_errors=(),
        stable=True,
        deprecated=False,
        description="じゃんけん単体の新しいメモリ上セッションを開始する。",
        tags=("janken", "session"),
    ),
)
