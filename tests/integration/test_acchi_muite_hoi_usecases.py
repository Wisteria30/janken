import pytest

from packages.acchi_muite_hoi.composition import create_acchi_muite_hoi_usecases
from packages.acchi_muite_hoi.usecases.play_acchi_muite_hoi_turn.v1 import (
    play_acchi_muite_hoi_turn_contract as acchi_play,
)
from packages.acchi_muite_hoi.usecases.start_acchi_muite_hoi_session.v1 import (
    start_acchi_muite_hoi_session_contract as acchi_start,
)


@pytest.mark.asyncio
async def test_acchi_muite_hoi_moves_to_direction_after_janken_win() -> None:
    usecases = create_acchi_muite_hoi_usecases(system_hands=["チョキ"], system_directions=["上"])
    caller = usecases.caller(None)

    started = await caller.call(
        acchi_start.START_ACCHI_MUITE_HOI_SESSION_USECASE,
        acchi_start.StartAcchiMuiteHoiSessionUseCaseInput(),
    )
    played = await caller.call(
        acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
        acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
            session_id=started.session_id,
            user_hand="グー",
            user_direction=None,
        ),
    )

    assert played.status == "waiting_for_look_direction"
    assert played.janken_result == "ユーザーの勝ち"
    assert played.initiative == "user"


@pytest.mark.asyncio
async def test_acchi_muite_hoi_finishes_when_direction_matches() -> None:
    usecases = create_acchi_muite_hoi_usecases(system_hands=["チョキ"], system_directions=["上"])
    caller = usecases.caller(None)
    started = await caller.call(
        acchi_start.START_ACCHI_MUITE_HOI_SESSION_USECASE,
        acchi_start.StartAcchiMuiteHoiSessionUseCaseInput(),
    )
    await caller.call(
        acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
        acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
            session_id=started.session_id,
            user_hand="グー",
            user_direction=None,
        ),
    )

    final = await caller.call(
        acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
        acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
            session_id=started.session_id,
            user_hand=None,
            user_direction="上",
        ),
    )

    assert final.status == "finished"
    assert final.system_direction == "上"
    assert final.final_result == "ユーザーの勝ち"


@pytest.mark.asyncio
async def test_acchi_muite_hoi_returns_to_janken_when_direction_differs() -> None:
    usecases = create_acchi_muite_hoi_usecases(system_hands=["パー"], system_directions=["右"])
    caller = usecases.caller(None)
    started = await caller.call(
        acchi_start.START_ACCHI_MUITE_HOI_SESSION_USECASE,
        acchi_start.StartAcchiMuiteHoiSessionUseCaseInput(),
    )
    await caller.call(
        acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
        acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
            session_id=started.session_id,
            user_hand="グー",
            user_direction=None,
        ),
    )

    continued = await caller.call(
        acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
        acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
            session_id=started.session_id,
            user_hand=None,
            user_direction="上",
        ),
    )

    assert continued.status == "waiting_for_janken_hand"
    assert continued.final_result is None


@pytest.mark.asyncio
async def test_acchi_muite_hoi_rejects_direction_in_janken_state() -> None:
    usecases = create_acchi_muite_hoi_usecases(system_hands=["グー"], system_directions=["上"])
    caller = usecases.caller(None)
    started = await caller.call(
        acchi_start.START_ACCHI_MUITE_HOI_SESSION_USECASE,
        acchi_start.StartAcchiMuiteHoiSessionUseCaseInput(),
    )

    with pytest.raises(acchi_play.AcchiMuiteHoiInputStateMismatchError):
        await caller.call(
            acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
            acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
                session_id=started.session_id,
                user_hand=None,
                user_direction="上",
            ),
        )


@pytest.mark.asyncio
async def test_acchi_muite_hoi_finished_session_is_error() -> None:
    usecases = create_acchi_muite_hoi_usecases(system_hands=["チョキ"], system_directions=["上"])
    caller = usecases.caller(None)
    started = await caller.call(
        acchi_start.START_ACCHI_MUITE_HOI_SESSION_USECASE,
        acchi_start.StartAcchiMuiteHoiSessionUseCaseInput(),
    )
    await caller.call(
        acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
        acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
            session_id=started.session_id,
            user_hand="グー",
            user_direction=None,
        ),
    )
    await caller.call(
        acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
        acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
            session_id=started.session_id,
            user_hand=None,
            user_direction="上",
        ),
    )

    with pytest.raises(acchi_play.AcchiMuiteHoiSessionAlreadyFinishedError):
        await caller.call(
            acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
            acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
                session_id=started.session_id,
                user_hand=None,
                user_direction="上",
            ),
        )
