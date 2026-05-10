"""あっち向いてほいセッションの現在状態に応じて、じゃんけんまたは方向勝負を 1 ステップ進める。"""

from __future__ import annotations

from packages.acchi_muite_hoi.domain.rules import Initiative, judge_direction
from packages.acchi_muite_hoi.domain.system_direction import SystemDirectionProvider
from packages.acchi_muite_hoi.usecases.play_acchi_muite_hoi_turn.v1 import (
    play_acchi_muite_hoi_turn_contract as contract,
)
from packages.acchi_muite_hoi.usecases.session_store import (
    AcchiMuiteHoiSession,
    AcchiMuiteHoiSessionStore,
)
from packages.janken.domain.rules import judge_janken
from packages.janken.domain.system_hand import SystemHandProvider


class PlayAcchiMuiteHoiTurnUseCase:
    """あっち向いてほいを 1 ステップ進める。"""

    def __init__(
        self,
        store: AcchiMuiteHoiSessionStore,
        system_hands: SystemHandProvider,
        system_directions: SystemDirectionProvider,
    ) -> None:
        self._store = store
        self._system_hands = system_hands
        self._system_directions = system_directions

    async def __call__(
        self, input: contract.PlayAcchiMuiteHoiTurnUseCaseInput, /
    ) -> contract.PlayAcchiMuiteHoiTurnUseCaseOutput:
        session = self._store.get(input.session_id)
        if session is None:
            raise contract.AcchiMuiteHoiSessionNotFoundError()
        if session.status == "finished":
            raise contract.AcchiMuiteHoiSessionAlreadyFinishedError()
        if session.status == "waiting_for_janken_hand":
            return self._play_janken(input)
        return self._play_direction(input)

    def _play_janken(
        self,
        input: contract.PlayAcchiMuiteHoiTurnUseCaseInput,
    ) -> contract.PlayAcchiMuiteHoiTurnUseCaseOutput:
        if input.user_hand is None or input.user_direction is not None:
            raise contract.AcchiMuiteHoiInputStateMismatchError()

        session = self._require_session(input.session_id)
        system_hand = self._system_hands.next_hand()
        result = judge_janken(input.user_hand, system_hand)
        initiative: Initiative | None = None
        message = "あいこです。もう一度じゃんけんの手を入力してください。"

        if result == "ユーザーの勝ち":
            initiative = "user"
            session.initiative = initiative
            session.status = "waiting_for_look_direction"
            message = "ユーザーが主導権を持ちました。方向を入力してください。"
        elif result == "ユーザーの負け":
            initiative = "system"
            session.initiative = initiative
            session.system_direction = self._system_directions.next_direction()
            session.status = "waiting_for_look_direction"
            message = "システムが主導権を持ちました。回避する方向を入力してください。"

        return contract.PlayAcchiMuiteHoiTurnUseCaseOutput(
            session_id=session.id,
            status=session.status,
            janken_result=result,
            initiative=initiative,
            user_hand=input.user_hand,
            system_hand=system_hand,
            user_direction=None,
            system_direction=None,
            final_result=None,
            message=message,
        )

    def _play_direction(
        self,
        input: contract.PlayAcchiMuiteHoiTurnUseCaseInput,
    ) -> contract.PlayAcchiMuiteHoiTurnUseCaseOutput:
        if input.user_hand is not None or input.user_direction is None:
            raise contract.AcchiMuiteHoiInputStateMismatchError()

        session = self._require_session(input.session_id)
        if session.initiative is None:
            raise contract.AcchiMuiteHoiInputStateMismatchError()
        system_direction = (
            self._system_directions.next_direction()
            if session.initiative == "user"
            else session.system_direction
        )
        if system_direction is None:
            raise contract.AcchiMuiteHoiInputStateMismatchError()

        final_result = judge_direction(session.initiative, input.user_direction, system_direction)
        if final_result is None:
            session.status = "waiting_for_janken_hand"
            session.initiative = None
            session.system_direction = None
            message = "方向が一致しませんでした。じゃんけんからやり直します。"
        else:
            session.status = "finished"
            message = f"最終結果は{final_result}です。"

        return contract.PlayAcchiMuiteHoiTurnUseCaseOutput(
            session_id=session.id,
            status=session.status,
            janken_result=None,
            initiative=session.initiative,
            user_hand=None,
            system_hand=None,
            user_direction=input.user_direction,
            system_direction=system_direction,
            final_result=final_result,
            message=message,
        )

    def _require_session(self, session_id: str) -> AcchiMuiteHoiSession:
        session = self._store.get(session_id)
        if session is None:
            raise contract.AcchiMuiteHoiSessionNotFoundError()
        return session


_impl: contract.PlayAcchiMuiteHoiTurn | None = None
