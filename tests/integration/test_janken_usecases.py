import pytest

from packages.janken.composition import create_janken_usecases
from packages.janken.usecases.play_janken_hand.v1.play_janken_hand_contract import (
    PLAY_JANKEN_HAND_USECASE,
    JankenSessionAlreadyFinishedError,
    JankenSessionNotFoundError,
    PlayJankenHandUseCaseInput,
)
from packages.janken.usecases.start_janken_session.v1.start_janken_session_contract import (
    START_JANKEN_SESSION_USECASE,
    StartJankenSessionUseCaseInput,
)


@pytest.mark.asyncio
async def test_janken_session_starts_and_finishes_with_user_win() -> None:
    usecases = create_janken_usecases(system_hands=["チョキ"])
    caller = usecases.caller(None)

    started = await caller.call(START_JANKEN_SESSION_USECASE, StartJankenSessionUseCaseInput())
    played = await caller.call(
        PLAY_JANKEN_HAND_USECASE,
        PlayJankenHandUseCaseInput(session_id=started.session_id, user_hand="グー"),
    )

    assert started.status == "waiting_for_user_hand"
    assert played.system_hand == "チョキ"
    assert played.result == "ユーザーの勝ち"
    assert played.status == "finished"


@pytest.mark.asyncio
async def test_janken_draw_keeps_same_session_waiting() -> None:
    usecases = create_janken_usecases(system_hands=["グー"])
    caller = usecases.caller(None)

    started = await caller.call(START_JANKEN_SESSION_USECASE, StartJankenSessionUseCaseInput())
    played = await caller.call(
        PLAY_JANKEN_HAND_USECASE,
        PlayJankenHandUseCaseInput(session_id=started.session_id, user_hand="グー"),
    )

    assert played.session_id == started.session_id
    assert played.result == "あいこ"
    assert played.status == "waiting_for_user_hand"


@pytest.mark.asyncio
async def test_janken_unknown_session_is_error() -> None:
    usecases = create_janken_usecases(system_hands=["グー"])
    caller = usecases.caller(None)

    with pytest.raises(JankenSessionNotFoundError):
        await caller.call(
            PLAY_JANKEN_HAND_USECASE,
            PlayJankenHandUseCaseInput(session_id="missing", user_hand="グー"),
        )


@pytest.mark.asyncio
async def test_janken_finished_session_is_error() -> None:
    usecases = create_janken_usecases(system_hands=["チョキ", "パー"])
    caller = usecases.caller(None)
    started = await caller.call(START_JANKEN_SESSION_USECASE, StartJankenSessionUseCaseInput())
    await caller.call(
        PLAY_JANKEN_HAND_USECASE,
        PlayJankenHandUseCaseInput(session_id=started.session_id, user_hand="グー"),
    )

    with pytest.raises(JankenSessionAlreadyFinishedError):
        await caller.call(
            PLAY_JANKEN_HAND_USECASE,
            PlayJankenHandUseCaseInput(session_id=started.session_id, user_hand="グー"),
        )
