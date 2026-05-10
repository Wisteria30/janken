from __future__ import annotations

from collections.abc import Sequence

from usecaseapi import UseCaseAPI

from packages.janken.domain.rules import Hand
from packages.janken.domain.system_hand import RandomSystemHandProvider, SequenceSystemHandProvider
from packages.janken.usecases.play_janken_hand.v1.play_janken_hand_contract import (
    PLAY_JANKEN_HAND_USECASE,
)
from packages.janken.usecases.play_janken_hand.v1.play_janken_hand_usecase import (
    PlayJankenHandUseCase,
)
from packages.janken.usecases.session_store import JankenSessionStore
from packages.janken.usecases.start_janken_session.v1.start_janken_session_contract import (
    START_JANKEN_SESSION_USECASE,
)
from packages.janken.usecases.start_janken_session.v1.start_janken_session_usecase import (
    StartJankenSessionUseCase,
)


def create_janken_usecases(system_hands: Sequence[Hand] | None = None) -> UseCaseAPI[None]:
    store = JankenSessionStore()
    hand_provider = (
        RandomSystemHandProvider()
        if system_hands is None
        else SequenceSystemHandProvider(system_hands)
    )
    usecases: UseCaseAPI[None] = UseCaseAPI()
    usecases.bind(
        START_JANKEN_SESSION_USECASE,
        lambda caller: StartJankenSessionUseCase(store),
    )
    usecases.bind(
        PLAY_JANKEN_HAND_USECASE,
        lambda caller: PlayJankenHandUseCase(store, hand_provider),
    )
    usecases.validate()
    return usecases


usecases = create_janken_usecases()
