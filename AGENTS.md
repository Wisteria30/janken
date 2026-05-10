# Agent Guidelines

このファイルは、この `janken` リポジトリで AI エージェントと人間の開発者が作業するための指針を定義する。
このリポジトリは `usecaseapi` を中心にした、じゃんけん CLI / HTTP アプリケーションである。

YAGNI、KISS、DRY、SOLID を優先する。読みやすく、検証しやすく、責務が明確なコードを書く。
合意のない代替動作はバグである。未指定の挙動を親切そうに作り込まない。

## Language And Encoding

- 作業説明、PR 説明、ドキュメント、コードコメントは日本語を基本にする。
- Python の識別子、公開 API 名、エラー型、設定キー、CLI コマンドは英語で明確に命名する。
- 外部に見えるメッセージは、既存の CLI / HTTP レスポンスの文脈に合わせる。
- すべてのテキストファイルは UTF-8 とする。
- 完了報告では、曖昧な目視確認だけを根拠にしない。実行したコマンドと結果を明記する。

## Repository Purpose

このリポジトリは、じゃんけんと「あっち向いてほい」を題材に、各機能 package のユースケースを CLI と FastAPI HTTP インターフェースから呼び出すアプリケーションである。

主要な関心事は次の通り。

- ドメインルール: 手、方向、勝敗、あいこ、主導権、最終勝敗の判断。
- ユースケース: 機能 package ごとに公開するアプリケーション操作。
- インターフェース: Typer などを使う CLI と FastAPI の HTTP API。
- 検証: ドメイン、ユースケース、CLI、HTTP の境界を分けたテスト。

このリポジトリを複数の配布単位の集合として扱わない。変更は原則として、単一プロジェクト内の機能 package と `app_shell` の責務に閉じる。

## Project Structure

現時点の設定上、次の構成を正とする。

- `pyproject.toml`: プロジェクト定義、依存関係、Ruff、mypy、pytest、エントリポイント。
- `uv.lock`: `uv` のロックファイル。依存関係を変えたら整合させる。
- `README.md`: ユーザー向けのセットアップ、CLI、HTTP、検証手順。
- `AGENTS.md`: 開発者と AI エージェント向けの作業指針。
- `.python-version`: このリポジトリで使う Python バージョン。

実装を追加する場合は、`src/packages/<feature_package>` と `src/app_shell` の二段構成を正とする。

- `src/packages/janken/domain/`: じゃんけんの純粋なルール。
- `src/packages/janken/usecases/`: じゃんけんのユースケースと入出力 DTO。
- `src/packages/janken/interfaces/`: じゃんけん用の CLI、HTTP router、表示、リクエスト/レスポンス変換。
- `src/packages/janken/composition.py`: じゃんけんのユースケース組み立て。
- `src/packages/acchi_muite_hoi/domain/`: あっち向いてほい固有の純粋なルール。
- `src/packages/acchi_muite_hoi/usecases/`: あっち向いてほいのユースケースと入出力 DTO。
- `src/packages/acchi_muite_hoi/interfaces/`: あっち向いてほい用の CLI、HTTP router、表示、リクエスト/レスポンス変換。
- `src/packages/acchi_muite_hoi/composition.py`: あっち向いてほいのユースケース組み立て。
- `src/app_shell/http.py`: 各機能 package の FastAPI router を統合する HTTP アプリケーション。
- `src/app_shell/cli.py`: 各機能 package の CLI を統合するトップレベル CLI。
- `tests/unit/`: 外部 I/O を使わない単体テスト。
- `tests/integration/`: ユースケース、HTTP、CLI など境界をまたぐ検証。
- `tests/e2e/`: 実際のコマンドや HTTP サーバーを使う検証。

Python の import package 名にはハイフンを使えない。package ディレクトリは `acchi_muite_hoi` のように `snake_case` とし、配布名、CLI コマンド名、HTTP path では必要に応じて `acchi-muite-hoi` を使ってよい。

生成物やローカルキャッシュをコミットしない。特に `.venv/`、`.mypy_cache/`、`.pytest_cache/`、`.ruff_cache/`、`__pycache__/`、`*.pyc`、`.coverage`、`htmlcov/`、`build/`、`dist/`、`*.egg-info/`、`.env`、`.env.*`、資格情報、トークン DB は含めない。

## Architecture Principles

- ドメインルールは CLI、HTTP、乱数、標準入力、標準出力、FastAPI に依存させない。
- 各機能 package の CLI と HTTP は同じユースケースを呼ぶ。片方だけに業務ルールを入れない。
- 各機能 package は、自分の domain、usecases、interfaces、composition を持つ。
- `src/app_shell` は統合だけを担当する。ドメイン判断やユースケース本体を置かない。
- FastAPI は各機能 package が `APIRouter` を公開し、`src/app_shell/http.py` が `include_router` で統合する。
- Typer などの CLI は各機能 package が subcommand 用の app を公開し、`src/app_shell/cli.py` が統合する。
- 完全に独立した ASGI アプリとして扱う明確な理由がない限り、機能 package ごとに `FastAPI()` 本体を作って `mount` しない。
- `acchi_muite_hoi` がじゃんけんの手や勝敗判定を使う場合は、`acchi_muite_hoi` から `janken` へ依存する。`janken` から `acchi_muite_hoi` へ依存させない。
- 公開境界は明示的に保つ。ユースケースの入力、出力、例外を曖昧にしない。
- ランダムな相手の手や方向は、テストで制御できる境界に切り出す。
- セッション状態を扱う場合は、責務と寿命を明確にする。暗黙のグローバル状態を増やさない。
- I/O、表示、HTTP 変換、ドメイン判断を混ぜない。
- 例外を握りつぶさない。未対応入力、不正な状態、未実装の操作は明示的に失敗させる。
- 合意されていない補完、再試行、別経路への切り替え、ダミーデータ返却は行わない。
- 抽象化は、実際の重複削減または複雑性低下がある場合だけ追加する。

## Python Rules

- Python は `pyproject.toml` の `requires-python` を正とする。現時点では `>=3.12`。
- 依存関係管理は `uv` を使う。`requirements.txt` は追加しない。
- `pyproject.toml` と `uv.lock` は整合させる。依存関係を変えたら `uv lock` または `uv sync` の結果を確認する。
- 型注釈を省略しない。`Any` は外部 SDK、動的 API、型表現が困難な境界に限定する。
- Pydantic を使う場合は v2 の記法に合わせる。
- async が必要な境界は FastAPI 側に閉じる。純粋なドメイン処理は同期関数でよい。
- コメントは「なぜそうしたか」を説明するために書く。コードを読めば分かる処理説明は避ける。
- テスト用の mock、stub、fake、placeholder を production code に置かない。

## Style And Naming

- Python は 4 スペースインデント、可能な限りダブルクォート、読みやすい行長を守る。
- `snake_case` をモジュール、関数、変数に使う。
- `PascalCase` をクラスに使う。
- `UPPER_SNAKE_CASE` を定数に使う。
- Ruff の設定は `pyproject.toml` を正とする。
- mypy は strict 設定を前提にする。型エラーを隠すための設定緩和はしない。
- ユーザー入力の日本語値は、表記ゆれを勝手に受け入れない。受け入れる値を増やす場合は仕様として明記し、テストを追加する。

## Testing Guidelines

- 変更した挙動には、成功経路、重要な失敗経路、境界条件の確認を追加する。
- ドメインルールは単体テストで確認する。
- CLI と HTTP は、ドメインルールの再テストではなく、入出力変換とユースケース呼び出しの境界を確認する。
- ランダム性はテストで制御できるようにする。結果が偶然に依存するテストを書かない。
- テストを削除したり、検証を弱めたり、チェック対象から除外して通すことを目的にしない。
- 実装がまだ存在しない領域では、変更範囲に合う最小の pytest 構成を追加してよい。

## Development Commands

依存関係の同期:

```bash
uv sync --group dev
```

二段構成へ移行後の CLI 実行例:

```bash
uv run games janken
uv run games acchi-muite-hoi
```

HTTP API の実行:

```bash
uv run uvicorn app_shell.http:app --reload
```

ユースケース定義の確認コマンドを用意している場合:

```bash
uv run usecaseapi check packages.janken.composition:usecases
uv run usecaseapi check packages.acchi_muite_hoi.composition:usecases
```

通常の検証:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

テスト種別を分けて確認する場合:

```bash
uv run pytest tests/unit
uv run pytest tests/integration
uv run pytest tests/e2e
```

存在しない一括コマンドを前提にしない。コマンドが現在のファイル構成で実行不能な場合は、理由を明記する。

## Documentation Rules

- README には、実際に再現できる手順を書く。
- CLI コマンド、HTTP エンドポイント、リクエスト例、レスポンス例は実装と一致させる。
- 個人の絶対パス、個人シェル設定、非公開サービス、メンテナだけが持つ認証情報を前提にしない。
- 生成物をコミットする場合は、元データと再生成コマンドを明記する。
- 仕様メモを書く場合は、採用した選択肢、捨てた選択肢、未決事項を分ける。

## Security And Configuration

- 秘密情報、API キー、トークン、個人アカウント値、`.env`、資格情報ファイルをコミットしない。
- README やログに実値を貼らない。例は `example.com` などの無害な値にする。
- 外部サービスを導入する場合は、入力値、失敗時の例外、再試行有無、権限範囲を明確にする。
- 認証失敗時に匿名アクセスや別資格情報へ自動で切り替えない。

## Git And PR Workflow

- 作業前に `git status --short` を確認し、既存の未コミット変更を壊さない。
- ブランチ名は作業内容を表すものにする。例: `feat/acchi-muite-hoi-cli`、`fix/http-session-state`、`docs/update-readme`。
- コミットメッセージは Conventional Commits を推奨する。例: `feat: add janken http session`。
- PR には目的、背景、主要変更、影響範囲、検証コマンド、未確認事項を書く。
- 挙動変更と大規模リファクタは、可能な限り分ける。

## AI Governance Rules

- 計画を出す前に、理想状態、現在の事実、差分、作業範囲、完了証拠を整理する。
- 完了を主張する前に、最新の差分と検証結果を確認する。
- 実装内容と実際の差分が一致しているか確認する。
- production code に mock、stub、fake、placeholder、合意のない代替動作を入れない。
- 実装と検証が終わる前に、完了したように読めるステータスやドキュメント更新をしない。
- 証拠が足りない場合は、完了ではなく部分完了として、残りの確認や判断事項を明記する。
