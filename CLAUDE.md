# FastAPI チュートリアル

## 目的
FastAPIの基礎を順番に学ぶ練習プロジェクト。

## 環境
- Python 3.9（str | None ではなく Optional[str] を使う）
- 仮想環境: venv/

## 学習スケジュール

### 基礎編（完了）
- [x] 環境構築・最初のAPI起動
- [x] パスパラメータ・クエリパラメータ
- [x] POSTリクエスト・Pydanticモデル
- [x] 入力・出力モデルを分ける
- [x] response_model でレスポンス制御
- [x] HTTPException でエラーハンドリング
- [x] 依存性注入（Depends）の基本
- [x] 依存性注入の応用（Headerトークン認証）

### DB連携編（完了）
- [x] SQLModelでDB連携（SQLite）
- [x] CRUD（POST / GET / PATCH / DELETE）
- [x] 入力・DBモデルの分離（HeroBase / HeroCreate / Hero）
- [x] Field によるバリデーション

### 実践編（完了）
- [x] 環境変数・設定管理（pydantic-settings）
- [x] ミドルウェア
- [x] CORS設定
- [x] lifespan
- [x] カスタム例外ハンドラー

### 残り
- [ ] ルーター（APIRouter）でファイルを分割
- [ ] テスト（pytest）
- [ ] JWT認証（OAuth2）
- [ ] favorite_books プロジェクトの構造を自分で再現する


## 今日の進捗（2026-06-10）
- [x] FastAPIインストール・サーバー起動
- [x] GETエンドポイント作成
- [x] パスパラメータ（型バリデーション確認）
- [x] クエリパラメータ（Optional[str]）
- [ ] POSTリクエスト・Pydanticモデル

## 学習メモ
- `str | None` はPython 3.10以上の書き方。3.9では `Optional[str]` を使う
- 型ヒントを書くだけで自動バリデーションが動く
- `--reload` でコード変更時にサーバーが自動再起動する
- [x] POSTリクエスト・Pydanticモデル  ← 次回ここから

## 今日の進捗（2026-06-12）
- [x] POSTリクエスト・Pydanticモデル
- [x] 入力・出力モデルを分ける（ItemCreate / ItemResponse）
- [x] response_model でレスポンスを制御
- [x] HTTPException でエラーハンドリング
- [x] 依存性注入（Depends）の基本

## 次回から
- [ ] 依存性注入の応用（認証への活用）
- [ ] データベース連携

## 今日の進捗（2026-06-13）
- [x] 依存性注入の応用（Headerを使ったトークン認証）
- [x] SQLModelでDB連携（SQLite）
- [x] DBへの保存・取得（POST / GET）
- [x] 入力・DBモデルの分離（HeroBase / HeroCreate / Hero）
- [x] 更新（PUT/PATCH）・削除（DELETE）エンドポイント
- [x] バリデーションの詳細（Field, validator）
- [x] 環境変数・設定管理
- [x] ミドルウェア（処理時間計測）
- [x] CORS設定
- [x] lifespan（起動・終了時の処理）
- [x] カスタム例外ハンドラー

## 次回から
- [ ] ルーター（APIRouter）でファイルを分割
- [ ] テスト（pytest）

### 今日の進捗（2026-06-14）
- [x] ルーター（APIRouter）でファイルを分割
- [x] テスト（pytest）
- [x] JWT認証（OAuth2）
- [ ] favorite_books プロジェクトの構造を自分で再現する