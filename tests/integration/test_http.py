from fastapi.testclient import TestClient

from app_shell.http import create_app


def test_http_janken_session_flow_finishes() -> None:
    client = TestClient(create_app(janken_system_hands=["チョキ"]))

    started = client.post("/sessions")
    session_id = started.json()["session_id"]
    played = client.post(f"/sessions/{session_id}/hands", json={"hand": "グー"})

    assert started.status_code == 200
    assert played.status_code == 200
    assert played.json()["result"] == "ユーザーの勝ち"
    assert played.json()["status"] == "finished"


def test_http_unknown_janken_session_is_404() -> None:
    client = TestClient(create_app(janken_system_hands=["グー"]))

    response = client.post("/sessions/missing/hands", json={"hand": "グー"})

    assert response.status_code == 404


def test_http_acchi_muite_hoi_state_mismatch_is_409() -> None:
    client = TestClient(
        create_app(acchi_system_hands=["グー"], acchi_system_directions=["上"]),
    )

    started = client.post("/acchi-muite-hoi/sessions")
    session_id = started.json()["session_id"]
    response = client.post(
        f"/acchi-muite-hoi/sessions/{session_id}/turns",
        json={"direction": "上"},
    )

    assert response.status_code == 409
