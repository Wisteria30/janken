from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from uuid import uuid4

from packages.acchi_muite_hoi.domain.rules import Direction, Initiative

type AcchiMuiteHoiSessionStatus = Literal[
    "waiting_for_janken_hand",
    "waiting_for_look_direction",
    "finished",
]


@dataclass
class AcchiMuiteHoiSession:
    id: str
    status: AcchiMuiteHoiSessionStatus
    initiative: Initiative | None = None
    system_direction: Direction | None = None


class AcchiMuiteHoiSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, AcchiMuiteHoiSession] = {}

    def create(self) -> AcchiMuiteHoiSession:
        session = AcchiMuiteHoiSession(id=uuid4().hex, status="waiting_for_janken_hand")
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> AcchiMuiteHoiSession | None:
        return self._sessions.get(session_id)
