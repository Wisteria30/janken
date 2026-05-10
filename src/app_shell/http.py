from __future__ import annotations

from collections.abc import Sequence

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

from app_shell.composition import create_usecases
from packages.acchi_muite_hoi.domain.rules import Direction
from packages.acchi_muite_hoi.usecases.play_acchi_muite_hoi_turn.v1 import (
    play_acchi_muite_hoi_turn_contract as acchi_play,
)
from packages.acchi_muite_hoi.usecases.start_acchi_muite_hoi_session.v1 import (
    start_acchi_muite_hoi_session_contract as acchi_start,
)
from packages.janken.domain.rules import Hand
from packages.janken.usecases.play_janken_hand.v1 import play_janken_hand_contract as janken_play
from packages.janken.usecases.start_janken_session.v1 import (
    start_janken_session_contract as janken_start,
)


class HandRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hand: Hand


class AcchiMuiteHoiTurnRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hand: Hand | None = None
    direction: Direction | None = None


def create_app(
    *,
    janken_system_hands: Sequence[Hand] | None = None,
    acchi_system_hands: Sequence[Hand] | None = None,
    acchi_system_directions: Sequence[Direction] | None = None,
) -> FastAPI:
    app = FastAPI(title="Janken")
    usecases = create_usecases(
        janken_system_hands=janken_system_hands,
        acchi_system_hands=acchi_system_hands,
        acchi_system_directions=acchi_system_directions,
    )

    @app.post("/sessions")
    async def start_janken_session() -> object:
        caller = usecases.caller(None)
        return await caller.call(
            janken_start.START_JANKEN_SESSION_USECASE,
            janken_start.StartJankenSessionUseCaseInput(),
        )

    @app.post("/sessions/{session_id}/hands")
    async def play_janken_hand(session_id: str, request: HandRequest) -> object:
        caller = usecases.caller(None)
        try:
            return await caller.call(
                janken_play.PLAY_JANKEN_HAND_USECASE,
                janken_play.PlayJankenHandUseCaseInput(
                    session_id=session_id,
                    user_hand=request.hand,
                ),
            )
        except janken_play.JankenSessionNotFoundError as exc:
            raise HTTPException(status_code=404, detail=exc.to_dict()) from exc
        except janken_play.JankenSessionAlreadyFinishedError as exc:
            raise HTTPException(status_code=409, detail=exc.to_dict()) from exc

    @app.post("/acchi-muite-hoi/sessions")
    async def start_acchi_muite_hoi_session() -> object:
        caller = usecases.caller(None)
        return await caller.call(
            acchi_start.START_ACCHI_MUITE_HOI_SESSION_USECASE,
            acchi_start.StartAcchiMuiteHoiSessionUseCaseInput(),
        )

    @app.post("/acchi-muite-hoi/sessions/{session_id}/turns")
    async def play_acchi_muite_hoi_turn(
        session_id: str,
        request: AcchiMuiteHoiTurnRequest,
    ) -> object:
        caller = usecases.caller(None)
        try:
            return await caller.call(
                acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
                acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
                    session_id=session_id,
                    user_hand=request.hand,
                    user_direction=request.direction,
                ),
            )
        except acchi_play.AcchiMuiteHoiSessionNotFoundError as exc:
            raise HTTPException(status_code=404, detail=exc.to_dict()) from exc
        except (
            acchi_play.AcchiMuiteHoiSessionAlreadyFinishedError,
            acchi_play.AcchiMuiteHoiInputStateMismatchError,
        ) as exc:
            raise HTTPException(status_code=409, detail=exc.to_dict()) from exc

    return app


app = create_app()
