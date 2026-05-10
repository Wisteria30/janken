"""既存のじゃんけんセッションにユーザーの手を適用し、システムの手と勝敗を返す。"""

from __future__ import annotations

from packages.janken.domain.rules import judge_janken
from packages.janken.domain.system_hand import SystemHandProvider
from packages.janken.usecases.play_janken_hand.v1.play_janken_hand_contract import (
    JankenSessionAlreadyFinishedError,
    JankenSessionNotFoundError,
    PlayJankenHand,
    PlayJankenHandUseCaseInput,
    PlayJankenHandUseCaseOutput,
)
from packages.janken.usecases.session_store import JankenSessionStore


class PlayJankenHandUseCase:
    """既存のじゃんけんセッションにユーザーの手を適用し、システムの手と勝敗を返す。"""

    def __init__(self, store: JankenSessionStore, system_hands: SystemHandProvider) -> None:
        self._store = store
        self._system_hands = system_hands

    async def __call__(self, input: PlayJankenHandUseCaseInput, /) -> PlayJankenHandUseCaseOutput:
        session = self._store.get(input.session_id)
        if session is None:
            raise JankenSessionNotFoundError()
        if session.status == "finished":
            raise JankenSessionAlreadyFinishedError()

        system_hand = self._system_hands.next_hand()
        result = judge_janken(input.user_hand, system_hand)
        if result == "あいこ":
            session.status = "waiting_for_user_hand"
            message = "あいこです。もう一度手を入力してください。"
        else:
            session.status = "finished"
            message = f"じゃんけんの結果は{result}です。"

        return PlayJankenHandUseCaseOutput(
            session_id=session.id,
            user_hand=input.user_hand,
            system_hand=system_hand,
            result=result,
            status=session.status,
            message=message,
        )


_impl: PlayJankenHand | None = None
