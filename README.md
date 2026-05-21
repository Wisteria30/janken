# Janken

UseCaseAPI で仕様書から Manifest を作り、Codex でじゃんけん / あっち向いてほいの CLI と HTTP API を実装する流れを体験できます。

## 作り方

再現手順は [docs/build_process.md](docs/build_process.md) にまとめています。

流れは次の通りです。

1. `uv sync --group dev` で依存関係を同期する。
2. Codex skill の [`usecaseapi-manifest-builder`](https://github.com/Wisteria30/usecaseapi/tree/main/.codex/skills/usecaseapi-manifest-builder) に [docs/spec_v1.md](docs/spec_v1.md) を渡して Manifest を作る。
3. `uv run usecaseapi manifest scaffold usecase.yaml --root .` で contract / implementation skeleton を生成する。
4. Codex に `ではusecaseに合わせて残りも [spec_v1.md](docs/spec_v1.md) について実装してください。` と依頼する。
5. テストと UseCaseAPI の同期確認で動作を確認する。

## 最小確認

```bash
uv sync --group dev
uv run pytest
uv run usecaseapi manifest check-sync app_shell.composition:usecases usecase.yaml
```

CLI を触る場合:

```bash
uv run janken
uv run acchi-muite-hoi
```

HTTP を触る場合:

```bash
uv run uvicorn app_shell.http:app --reload
```

Swagger UI は `http://127.0.0.1:8000/docs` から確認できます。
