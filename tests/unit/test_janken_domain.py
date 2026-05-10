from packages.janken.domain.rules import judge_janken


def test_judge_user_win() -> None:
    assert judge_janken("グー", "チョキ") == "ユーザーの勝ち"


def test_judge_user_lose() -> None:
    assert judge_janken("グー", "パー") == "ユーザーの負け"


def test_judge_draw() -> None:
    assert judge_janken("グー", "グー") == "あいこ"
