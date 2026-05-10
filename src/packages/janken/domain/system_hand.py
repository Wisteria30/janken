from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass

from packages.janken.domain.rules import HANDS, Hand


class SystemHandProvider:
    def next_hand(self) -> Hand:
        raise NotImplementedError


class RandomSystemHandProvider(SystemHandProvider):
    def next_hand(self) -> Hand:
        return random.choice(HANDS)


@dataclass
class SequenceSystemHandProvider(SystemHandProvider):
    hands: Sequence[Hand]
    index: int = 0

    def next_hand(self) -> Hand:
        if self.index >= len(self.hands):
            raise RuntimeError("system hand sequence is exhausted")
        hand = self.hands[self.index]
        self.index += 1
        return hand
