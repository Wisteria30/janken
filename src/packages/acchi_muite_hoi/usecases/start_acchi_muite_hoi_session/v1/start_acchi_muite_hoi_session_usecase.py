"""あっち向いてほいの新しいメモリ上セッションを開始する。"""

from __future__ import annotations

from packages.acchi_muite_hoi.usecases.session_store import AcchiMuiteHoiSessionStore
from packages.acchi_muite_hoi.usecases.start_acchi_muite_hoi_session.v1 import (
    start_acchi_muite_hoi_session_contract as contract,
)


class StartAcchiMuiteHoiSessionUseCase:
    """あっち向いてほいの新しいメモリ上セッションを開始する。"""

    def __init__(self, store: AcchiMuiteHoiSessionStore) -> None:
        self._store = store

    async def __call__(
        self, input: contract.StartAcchiMuiteHoiSessionUseCaseInput, /
    ) -> contract.StartAcchiMuiteHoiSessionUseCaseOutput:
        session = self._store.create()
        return contract.StartAcchiMuiteHoiSessionUseCaseOutput(
            session_id=session.id,
            status="waiting_for_janken_hand",
            message="あっち向いてほいを開始しました。じゃんけんの手を入力してください。",
        )


_impl: contract.StartAcchiMuiteHoiSession | None = None
