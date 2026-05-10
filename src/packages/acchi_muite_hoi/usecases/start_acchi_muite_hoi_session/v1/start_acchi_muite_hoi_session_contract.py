"""あっち向いてほいの新しいメモリ上セッションを開始する。"""

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


class StartAcchiMuiteHoiSessionUseCaseInput(Model):
    """あっち向いてほいセッション開始に必要な入力を表す。"""

    pass


class StartAcchiMuiteHoiSessionUseCaseOutput(Model):
    """開始されたあっち向いてほいセッションの識別子と初期状態を表す。"""

    session_id: str = Field(
        description="アプリケーション実行中のメモリ上でセッションを識別する値。"
    )
    status: Literal["waiting_for_janken_hand"] = Field(
        description="じゃんけんの手入力待ちであることを示す状態。"
    )
    message: str = Field(description="CLI または HTTP で利用する利用者向けメッセージ。")


class StartAcchiMuiteHoiSession(
    UseCase[StartAcchiMuiteHoiSessionUseCaseInput, StartAcchiMuiteHoiSessionUseCaseOutput], Protocol
):
    """あっち向いてほいの新しいメモリ上セッションを開始する。"""

    async def __call__(
        self, input: StartAcchiMuiteHoiSessionUseCaseInput, /
    ) -> StartAcchiMuiteHoiSessionUseCaseOutput: ...


START_ACCHI_MUITE_HOI_SESSION_USECASE: UseCaseRef[
    StartAcchiMuiteHoiSessionUseCaseInput, StartAcchiMuiteHoiSessionUseCaseOutput
] = define_usecase(
    StartAcchiMuiteHoiSession,
    Contract(
        name="packages.acchi_muite_hoi.start_acchi_muite_hoi_session",
        version=1,
        input=StartAcchiMuiteHoiSessionUseCaseInput,
        output=StartAcchiMuiteHoiSessionUseCaseOutput,
        raises=(),
        known_errors=(),
        stable=True,
        deprecated=False,
        description="あっち向いてほいの新しいメモリ上セッションを開始する。",
        tags=("acchi-muite-hoi", "session"),
    ),
)
