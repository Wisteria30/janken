from packages.acchi_muite_hoi.domain.rules import judge_direction


def test_judge_user_win_when_user_has_initiative_and_directions_match() -> None:
    assert judge_direction("user", "上", "上") == "ユーザーの勝ち"


def test_judge_user_lose_when_system_has_initiative_and_directions_match() -> None:
    assert judge_direction("system", "左", "左") == "ユーザーの負け"


def test_judge_direction_unresolved_when_directions_do_not_match() -> None:
    assert judge_direction("user", "上", "下") is None
