from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from uuid import uuid4

type JankenSessionStatus = Literal["waiting_for_user_hand", "finished"]


@dataclass
class JankenSession:
    id: str
    status: JankenSessionStatus


class JankenSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, JankenSession] = {}

    def create(self) -> JankenSession:
        session = JankenSession(id=uuid4().hex, status="waiting_for_user_hand")
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> JankenSession | None:
        return self._sessions.get(session_id)
