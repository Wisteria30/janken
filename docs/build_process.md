# 再現手順書

この手順書は、`docs/spec_v1.md` から現在の `janken` アプリを作るための作業順をまとめる。
考え方の説明ではなく、同じ流れをもう一度たどれることを目的にする。

## 0. 前提条件

開始時点で次がそろっていること。

- `AGENTS.md` がある。
- `uv` が使える。
- `pyproject.toml` と `uv.lock` がある。
- `usecaseapi` が依存関係に含まれている。
- 仕様書が `docs/spec_v1.md` のような形で存在する。
- リポジトリルートで作業できる。

## 1. 依存関係をそろえる

依存関係は `pyproject.toml` と `uv.lock` に従って同期する。

```bash
uv sync --group dev
```

## 2. Manifest はスキルで作る

Manifest は手で悩んで組み立てない。
[`usecaseapi-manifest-builder`](https://github.com/Wisteria30/usecaseapi/tree/main/.codex/skills/usecaseapi-manifest-builder) スキルに、仕様書を渡して作る。

依頼の形は次のようにする。

```text
[$usecaseapi-manifest-builder](https://github.com/Wisteria30/usecaseapi/tree/main/.codex/skills/usecaseapi-manifest-builder) [spec_v1.md](docs/spec_v1.md)
```

スキルにやらせること。

1. `docs/spec_v1.md` を読む。
2. 必要な対話を行い、ユースケースの境界、入力、出力、エラーを決める。
3. `usecaseapi.ucase.yaml` を作る。
4. `uv run usecaseapi manifest validate usecaseapi.ucase.yaml` を実行する。
5. `uv run usecaseapi manifest scaffold usecaseapi.ucase.yaml --root . --dry-run` で生成予定を出す。

Manifest に入れるのは、アプリケーション操作の公開契約だけ。
乱数生成器、セッションストア、CLI、HTTP、DB、リポジトリ、外部クライアントは `uses` に入れない。

## 3. 契約ファイルを生成する

まず生成予定を確認する。

```bash
uv run usecaseapi manifest scaffold usecaseapi.ucase.yaml --root . --dry-run
```

予定ファイルが `src/packages/.../usecases/.../v1/` 配下になっていることを確認する。
この `docs/spec_v1.md` では、例として次のような出力になる。

```text
created: src/packages/janken/usecases/start_janken_session/v1/start_janken_session_contract.py
created: src/packages/janken/usecases/start_janken_session/v1/start_janken_session_usecase.py
created: src/packages/janken/usecases/play_janken_hand/v1/play_janken_hand_contract.py
created: src/packages/janken/usecases/play_janken_hand/v1/play_janken_hand_usecase.py
created: src/packages/acchi_muite_hoi/usecases/start_acchi_muite_hoi_session/v1/start_acchi_muite_hoi_session_contract.py
created: src/packages/acchi_muite_hoi/usecases/start_acchi_muite_hoi_session/v1/start_acchi_muite_hoi_session_usecase.py
created: src/packages/acchi_muite_hoi/usecases/play_acchi_muite_hoi_turn/v1/play_acchi_muite_hoi_turn_contract.py
created: src/packages/acchi_muite_hoi/usecases/play_acchi_muite_hoi_turn/v1/play_acchi_muite_hoi_turn_usecase.py
```

問題なければ生成する。

```bash
uv run usecaseapi manifest scaffold usecaseapi.ucase.yaml --root .
```

この時点では implementation は未実装でよい。
生成後の contract は公開境界なので、以後は Manifest と同期させる。

## 4. Codex に残りを実装してもらう

生成後の詳細実装は、次の指示を Codex に投げる。

```text
ではusecaseに合わせて残りも [spec_v1.md](docs/spec_v1.md) について実装してください。
```

ユーザー側の手順としては、ここで実装の詳細を分解しない。
Codex が仕様、Manifest、生成済み contract に合わせて実装し、検証結果を報告する。

## 5. 動作確認する

Codex の実装後、最低限次を確認する。

```bash
uv run pytest
uv run usecaseapi manifest check-sync app_shell.composition:usecases usecaseapi.ucase.yaml
```

必要に応じて CLI または HTTP も起動して確認する。

```bash
uv run janken
uv run acchi-muite-hoi
uv run uvicorn app_shell.http:app --reload
```
