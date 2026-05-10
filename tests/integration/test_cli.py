import pytest
from typer.testing import CliRunner

from app_shell.cli import app


def test_janken_cli_finishes_with_user_win(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = CliRunner()
    monkeypatch.setattr("random.choice", lambda values: "チョキ")

    result = runner.invoke(app, ["janken"], input="グー\n")

    assert result.exit_code == 0
    assert "ユーザーの勝ち" in result.output


def test_acchi_muite_hoi_cli_finishes_with_user_win(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = CliRunner()
    choices = iter(["チョキ", "上"])
    monkeypatch.setattr("random.choice", lambda values: next(choices))

    result = runner.invoke(app, ["acchi-muite-hoi"], input="グー\n上\n")

    assert result.exit_code == 0
    assert "ユーザーの勝ち" in result.output
