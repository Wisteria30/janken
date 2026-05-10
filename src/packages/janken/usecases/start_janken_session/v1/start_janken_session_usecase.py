"""じゃんけん単体の新しいメモリ上セッションを開始する。"""

from __future__ import annotations

from packages.janken.usecases.session_store import JankenSessionStore
from packages.janken.usecases.start_janken_session.v1.start_janken_session_contract import (
    StartJankenSession,
    StartJankenSessionUseCaseInput,
    StartJankenSessionUseCaseOutput,
)


class StartJankenSessionUseCase:
    """じゃんけん単体の新しいメモリ上セッションを開始する。"""

    def __init__(self, store: JankenSessionStore) -> None:
        self._store = store

    async def __call__(
        self, input: StartJankenSessionUseCaseInput, /
    ) -> StartJankenSessionUseCaseOutput:
        session = self._store.create()
        return StartJankenSessionUseCaseOutput(
            session_id=session.id,
            status="waiting_for_user_hand",
            message="じゃんけんを開始しました。手を入力してください。",
        )


_impl: StartJankenSession | None = None
