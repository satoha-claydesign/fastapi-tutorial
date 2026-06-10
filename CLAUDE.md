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
