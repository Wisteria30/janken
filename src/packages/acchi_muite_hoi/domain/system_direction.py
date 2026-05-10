from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass

from packages.acchi_muite_hoi.domain.rules import DIRECTIONS, Direction


class SystemDirectionProvider:
    def next_direction(self) -> Direction:
        raise NotImplementedError


class RandomSystemDirectionProvider(SystemDirectionProvider):
    def next_direction(self) -> Direction:
        return random.choice(DIRECTIONS)


@dataclass
class SequenceSystemDirectionProvider(SystemDirectionProvider):
    directions: Sequence[Direction]
    index: int = 0

    def next_direction(self) -> Direction:
        if self.index >= len(self.directions):
            raise RuntimeError("system direction sequence is exhausted")
        direction = self.directions[self.index]
        self.index += 1
        return direction
