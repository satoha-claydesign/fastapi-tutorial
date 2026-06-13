# FastAPI チュートリアル

## 目的
FastAPIの基礎を順番に学ぶ練習プロジェクト。

## 環境
- Python 3.9（str | None ではなく Optional[str] を使う）
- 仮想環境: venv/

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

## 次回から
- [ ] 更新（PUT/PATCH）・削除（DELETE）エンドポイント
- [ ] バリデーションの詳細（Field, validator）
- [ ] 環境変数・設定管理