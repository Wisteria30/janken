from __future__ import annotations

import asyncio
from typing import Literal

import typer

from app_shell.composition import create_usecases
from packages.acchi_muite_hoi.usecases.play_acchi_muite_hoi_turn.v1 import (
    play_acchi_muite_hoi_turn_contract as acchi_play,
)
from packages.acchi_muite_hoi.usecases.start_acchi_muite_hoi_session.v1 import (
    start_acchi_muite_hoi_session_contract as acchi_start,
)
from packages.janken.usecases.play_janken_hand.v1 import play_janken_hand_contract as janken_play
from packages.janken.usecases.start_janken_session.v1 import (
    start_janken_session_contract as janken_start,
)

app = typer.Typer(no_args_is_help=True)


@app.command("janken")
def janken_command() -> None:
    asyncio.run(_run_janken())


@app.command("acchi-muite-hoi")
def acchi_muite_hoi_command() -> None:
    asyncio.run(_run_acchi_muite_hoi())


async def _run_janken() -> None:
    usecases = create_usecases()
    caller = usecases.caller(None)
    started = await caller.call(
        janken_start.START_JANKEN_SESSION_USECASE,
        janken_start.StartJankenSessionUseCaseInput(),
    )
    typer.echo(started.message)
    session_id = started.session_id

    while True:
        hand = typer.prompt("手")
        try:
            played = await caller.call(
                janken_play.PLAY_JANKEN_HAND_USECASE,
                janken_play.PlayJankenHandUseCaseInput(session_id=session_id, user_hand=hand),
            )
        except ValueError:
            typer.echo("不正な手です。グー、チョキ、パーのいずれかを入力してください。")
            continue
        typer.echo(f"ユーザー: {played.user_hand}")
        typer.echo(f"システム: {played.system_hand}")
        typer.echo(f"結果: {played.result}")
        typer.echo(played.message)
        if played.status == "finished":
            return


async def _run_acchi_muite_hoi() -> None:
    usecases = create_usecases()
    caller = usecases.caller(None)
    started = await caller.call(
        acchi_start.START_ACCHI_MUITE_HOI_SESSION_USECASE,
        acchi_start.StartAcchiMuiteHoiSessionUseCaseInput(),
    )
    typer.echo(started.message)
    session_id = started.session_id
    status: Literal["waiting_for_janken_hand", "waiting_for_look_direction", "finished"]
    status = started.status

    while True:
        if status == "waiting_for_janken_hand":
            raw_value = typer.prompt("手")
            user_hand = raw_value
            user_direction = None
        else:
            raw_value = typer.prompt("方向")
            user_hand = None
            user_direction = raw_value

        try:
            played = await caller.call(
                acchi_play.PLAY_ACCHI_MUITE_HOI_TURN_USECASE,
                acchi_play.PlayAcchiMuiteHoiTurnUseCaseInput(
                    session_id=session_id,
                    user_hand=user_hand,
                    user_direction=user_direction,
                ),
            )
        except ValueError:
            typer.echo("入力が不正です。現在の状態に合う値を入力してください。")
            continue
        except acchi_play.AcchiMuiteHoiInputStateMismatchError:
            typer.echo("現在の状態に合わない入力です。")
            continue

        if played.user_hand is not None and played.system_hand is not None:
            typer.echo(f"ユーザーの手: {played.user_hand}")
            typer.echo(f"システムの手: {played.system_hand}")
            typer.echo(f"じゃんけん結果: {played.janken_result}")
        if played.user_direction is not None and played.system_direction is not None:
            typer.echo(f"ユーザーの方向: {played.user_direction}")
            typer.echo(f"システムの方向: {played.system_direction}")
        if played.final_result is not None:
            typer.echo(f"結果: {played.final_result}")
        typer.echo(played.message)

        status = played.status
        if status == "finished":
            return


def main_janken() -> None:
    asyncio.run(_run_janken())


def main_acchi_muite_hoi() -> None:
    asyncio.run(_run_acchi_muite_hoi())
