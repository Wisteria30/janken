from __future__ import annotations

from collections.abc import Sequence

from usecaseapi import UseCaseAPI

from packages.acchi_muite_hoi.domain.rules import Direction
from packages.acchi_muite_hoi.domain.system_direction import (
    RandomSystemDirectionProvider,
    SequenceSystemDirectionProvider,
)
from packages.acchi_muite_hoi.usecases.play_acchi_muite_hoi_turn.v1 import (
    play_acchi_muite_hoi_turn_contract as turn_contract,
)
from packages.acchi_muite_hoi.usecases.play_acchi_muite_hoi_turn.v1 import (
    play_acchi_muite_hoi_turn_usecase as turn_usecase,
)
from packages.acchi_muite_hoi.usecases.session_store import AcchiMuiteHoiSessionStore
from packages.acchi_muite_hoi.usecases.start_acchi_muite_hoi_session.v1 import (
    start_acchi_muite_hoi_session_contract as start_contract,
)
from packages.acchi_muite_hoi.usecases.start_acchi_muite_hoi_session.v1 import (
    start_acchi_muite_hoi_session_usecase as start_usecase,
)
from packages.janken.domain.rules import Hand
from packages.janken.domain.system_hand import RandomSystemHandProvider, SequenceSystemHandProvider


def create_acchi_muite_hoi_usecases(
    *,
    system_hands: Sequence[Hand] | None = None,
    system_directions: Sequence[Direction] | None = None,
) -> UseCaseAPI[None]:
    store = AcchiMuiteHoiSessionStore()
    hand_provider = (
        RandomSystemHandProvider()
        if system_hands is None
        else SequenceSystemHandProvider(system_hands)
    )
    direction_provider = (
        RandomSystemDirectionProvider()
        if system_directions is None
        else SequenceSystemDirectionProvider(system_directions)
    )
    usecases: UseCaseAPI[None] = UseCaseAPI()
    usecases.bind(
        start_contract.START_ACCHI_MUITE_HOI_SESSION_USECASE,
        lambda caller: start_usecase.StartAcchiMuiteHoiSessionUseCase(store),
    )
    usecases.bind(
        turn_contract.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
        lambda caller: turn_usecase.PlayAcchiMuiteHoiTurnUseCase(
            store,
            hand_provider,
            direction_provider,
        ),
    )
    usecases.validate()
    return usecases


usecases = create_acchi_muite_hoi_usecases()
