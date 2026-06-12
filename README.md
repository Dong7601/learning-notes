# 学習ノート (learning-notes)

Claude Code / Codex との実装会話を、非エンジニアでも後から学べる形に整理した
ナレッジ集。GitHub Pages で公開し、スマホからも閲覧できる。

公開URL: https://dong7601.github.io/learning-notes/

## 構成

```
learning-notes/
├─ index.html          トップ：ノート一覧 + キーワード検索
├─ clips/              クリップフィード（生成HTML）
├─ notes/              個別ノート（HTML 1ファイル = 1テーマ）
│   └─ powerpoint-addin.html
├─ tools/              生成スクリプト
├─ robots.txt          検索エンジン除外（Disallow: /）
├─ .nojekyll           Jekyll 処理を無効化
└─ PUBLICATION_REVIEW.md  公開前の機密検閲ログ
```

## ノートの追加手順

1. `notes/<テーマ>.html` を作成（既存ノートをスタイル雛形にする）。
2. `<head>` に `<meta name="robots" content="noindex, nofollow">` を入れる。
3. ページ冒頭に「← 学習ノート一覧へ戻る」リンク（`../index.html`）を入れる。
4. `index.html` の `NOTES` 配列に1件追加（title / href / date / summary / tags）。
5. `PUBLICATION_REVIEW.md` に検閲結果を追記してから commit & push。

## 公開2大ルール（必須）

1. **機密検閲** … 会社名・取引先名・個人情報・秘密値が無いか全文確認し、伏字／削除。
2. **検索除外** … `robots.txt` の `Disallow: /` ＋ 全HTMLの `noindex,nofollow` メタ。

詳細は vault: `04_Context/AgentOps/Docs/github-pages-publish-rules.md`。

## クリップフィード

Obsidian の外部記事/X投稿クリップを `clips/index.html` に静的HTMLとして生成する。
ビルド: `python tools/build_clips.py --src <Obsidianのクリップフォルダ>`。
生成HTMLの `noindex, nofollow` は維持する。
公開対象は外部記事/X投稿の要約と公開URLのみ。備考段落は非公開、`memo` / `prompt` タイプは除外する。

## コンテンツ作成ルール

### 標準構成

戻るリンク → ヒーロー（メタ行） → TL;DR（結論先行） → 図解（最低1つ） → 本文 → 用語集 → footer。

### メタデータ

新ノートは `notes/_template.html` を複製して作り、`index.html` の `NOTES` に `title` / `href` / `date` / `summary` / `tags` / `category` / `level` を登録する。

### 難易度

`入門` / `基礎` / `応用` の3段階。

### カテゴリ

- `dev` = 開発・GitHub
- `ai` = AI・データ活用
- `office` = Office・自動化

カテゴリが増えたら `index.html` の `CATEGORIES` に追加する。

### ファイル名

半角小文字ケバブケースにする。例: `github-for-non-engineers.html`

### 必須

- `<head>` に `noindex,nofollow`
- 冒頭に戻るリンク
- 図解を最低1つ
- レスポンシブ
- アニメーションを入れる場合は `prefers-reduced-motion` 対応

### 公開2大ルール

1. **機密検閲**: 会社名・取引先・個人情報・秘密値を伏字または削除し、`PUBLICATION_REVIEW.md` に記録する。
2. **検索除外**: `robots.txt` と各HTMLの `noindex` で検索除外する。
