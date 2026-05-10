from __future__ import annotations

from collections.abc import Sequence

from usecaseapi import UseCaseAPI

from packages.acchi_muite_hoi.composition import create_acchi_muite_hoi_usecases
from packages.acchi_muite_hoi.domain.rules import Direction
from packages.janken.composition import create_janken_usecases
from packages.janken.domain.rules import Hand


def create_usecases(
    *,
    janken_system_hands: Sequence[Hand] | None = None,
    acchi_system_hands: Sequence[Hand] | None = None,
    acchi_system_directions: Sequence[Direction] | None = None,
) -> UseCaseAPI[None]:
    usecases: UseCaseAPI[None] = UseCaseAPI()
    for binding in create_janken_usecases(janken_system_hands).bindings:
        usecases.bind(binding.ref, binding.factory, uses=(), tags=binding.tags)
    for binding in create_acchi_muite_hoi_usecases(
        system_hands=acchi_system_hands,
        system_directions=acchi_system_directions,
    ).bindings:
        usecases.bind(binding.ref, binding.factory, uses=(), tags=binding.tags)
    usecases.validate()
    return usecases


usecases = create_usecases()
