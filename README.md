# 学習ノート (learning-notes)

Claude Code / Codex との実装会話を、非エンジニアでも後から学べる形に整理した
ナレッジ集。GitHub Pages で公開し、スマホからも閲覧できる。

公開URL: https://dong7601.github.io/learning-notes/

## 構成

```
learning-notes/
├─ index.html          トップ：ノート一覧 + キーワード検索
├─ notes/              個別ノート（HTML 1ファイル = 1テーマ）
│   └─ powerpoint-addin.html
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
