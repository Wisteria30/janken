"""あっち向いてほいセッションの現在状態に応じて、じゃんけんまたは方向勝負を 1 ステップ進める。"""

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

DESCRIPTION = (
    "あっち向いてほいセッションの現在状態に応じて、じゃんけんまたは方向勝負を 1 ステップ進める。"
)


class PlayAcchiMuiteHoiTurnUseCaseInput(Model):
    """あっち向いてほいセッションを現在状態に応じて 1 ステップ進めるための入力を表す。"""

    session_id: str = Field(description="対象のあっち向いてほいセッションを識別する値。")
    user_hand: Literal["グー", "チョキ", "パー"] | None = Field(
        description="じゃんけんの手入力待ち状態で指定するユーザーの手。"
    )
    user_direction: Literal["上", "下", "右", "左"] | None = Field(
        description="方向入力待ち状態で指定するユーザーの方向。"
    )


class PlayAcchiMuiteHoiTurnUseCaseOutput(Model):
    """あっち向いてほい 1 ステップ分の判定結果と次状態を表す。"""

    session_id: str = Field(description="対象のあっち向いてほいセッションを識別する値。")
    status: Literal["waiting_for_janken_hand", "waiting_for_look_direction", "finished"] = Field(
        description="次に必要な入力、または最終勝敗確定を示す状態。"
    )
    janken_result: Literal["ユーザーの勝ち", "ユーザーの負け", "あいこ"] | None = Field(
        description="じゃんけんを実行したステップでの勝敗。"
    )
    initiative: Literal["user", "system"] | None = Field(
        description="方向勝負に進む場合の主導権の所在。"
    )
    user_hand: Literal["グー", "チョキ", "パー"] | None = Field(
        description="じゃんけんを実行したステップで判定に使用されたユーザーの手。"
    )
    system_hand: Literal["グー", "チョキ", "パー"] | None = Field(
        description="じゃんけんを実行したステップで判定に使用されたシステムの手。"
    )
    user_direction: Literal["上", "下", "右", "左"] | None = Field(
        description="方向勝負を実行したステップで判定に使用されたユーザーの方向。"
    )
    system_direction: Literal["上", "下", "右", "左"] | None = Field(
        description="方向勝負を実行したステップで判定に使用されたシステムの方向。"
    )
    final_result: Literal["ユーザーの勝ち", "ユーザーの負け"] | None = Field(
        description="最終勝敗が確定した場合の結果。"
    )
    message: str = Field(description="CLI または HTTP で利用する利用者向けメッセージ。")


class AcchiMuiteHoiSessionError(UseCaseError):
    code: ClassVar[str] = "packages.acchi_muite_hoi.play_acchi_muite_hoi_turn.session_error"


class InvalidAcchiMuiteHoiHandError(AcchiMuiteHoiSessionError):
    code: ClassVar[str] = "packages.acchi_muite_hoi.play_acchi_muite_hoi_turn.invalid_hand"


class InvalidAcchiMuiteHoiDirectionError(AcchiMuiteHoiSessionError):
    code: ClassVar[str] = "packages.acchi_muite_hoi.play_acchi_muite_hoi_turn.invalid_direction"


class AcchiMuiteHoiSessionNotFoundError(AcchiMuiteHoiSessionError):
    code: ClassVar[str] = "packages.acchi_muite_hoi.play_acchi_muite_hoi_turn.session_not_found"


class AcchiMuiteHoiSessionAlreadyFinishedError(AcchiMuiteHoiSessionError):
    code: ClassVar[str] = (
        "packages.acchi_muite_hoi.play_acchi_muite_hoi_turn.session_already_finished"
    )


class AcchiMuiteHoiInputStateMismatchError(AcchiMuiteHoiSessionError):
    code: ClassVar[str] = "packages.acchi_muite_hoi.play_acchi_muite_hoi_turn.input_state_mismatch"


class PlayAcchiMuiteHoiTurn(
    UseCase[PlayAcchiMuiteHoiTurnUseCaseInput, PlayAcchiMuiteHoiTurnUseCaseOutput], Protocol
):
    """あっち向いてほいを 1 ステップ進める。"""

    async def __call__(
        self, input: PlayAcchiMuiteHoiTurnUseCaseInput, /
    ) -> PlayAcchiMuiteHoiTurnUseCaseOutput: ...


PLAY_ACCHI_MUITE_HOI_TURN_USECASE: UseCaseRef[
    PlayAcchiMuiteHoiTurnUseCaseInput, PlayAcchiMuiteHoiTurnUseCaseOutput
] = define_usecase(
    PlayAcchiMuiteHoiTurn,
    Contract(
        name="packages.acchi_muite_hoi.play_acchi_muite_hoi_turn",
        version=1,
        input=PlayAcchiMuiteHoiTurnUseCaseInput,
        output=PlayAcchiMuiteHoiTurnUseCaseOutput,
        raises=(AcchiMuiteHoiSessionError,),
        known_errors=(
            InvalidAcchiMuiteHoiHandError,
            InvalidAcchiMuiteHoiDirectionError,
            AcchiMuiteHoiSessionNotFoundError,
            AcchiMuiteHoiSessionAlreadyFinishedError,
            AcchiMuiteHoiInputStateMismatchError,
        ),
        stable=True,
        deprecated=False,
        description=DESCRIPTION,
        tags=("acchi-muite-hoi", "game-step"),
    ),
)
