# 公開前 機密検閲ログ (PUBLICATION_REVIEW)

公開するノートは、必ず以下の観点で全文確認してから push する。

- 会社名 / 取引先名 / 固有のプロジェクト名 / 部署名
- 個人名 / メール / 電話 / 住所などの連絡先
- Cookie / Token / APIキー / パスワード / 認証コード / 身分証番号 / 銀行情報
- ログ中の機密値、サードパーティの設定値

---

## 2026-06-12

### notes/powerpoint-addin.html
- 出所: office-addin-knowledge リポジトリからの移植（元々「公開用に匿名化済み」）。
- 検閲結果: 会社名・取引先名・個人情報なし。社内アドインは「社内配布アドイン」と
  一般化済み。固有名詞なし。**問題なし。**

### index.html / README.md / robots.txt
- 検閲結果: 機密情報なし。GitHubアカウント名（公開情報）のみ記載。**問題なし。**

### notes/ai-api-vs-subscription.html
- ai-api-vs-subscription：機密情報なし（一般教育内容。会社名・取引先・個人情報・秘密値を含まない）

### clips/index.html / tools/build_clips.py
- 公開対象は外部記事/X投稿の要約と公開URLのみ。
- 生成時に備考段落、`memo` / `prompt` タイプ、Slack permalink などの内部向けリンクは除外する。
- 生成HTMLは `noindex, nofollow` メタを維持する。ローカル絶対パスは出力しない。

### 検索除外
- robots.txt に `Disallow: /` を設置。
- 全HTMLの `<head>` に `noindex, nofollow` メタを設置。
- notes/_template.html：ひな型（プレースホルダのみ・機密情報なし）

---

## 2026-06-17

### notes/claude-dynamic-workflow-effort.html
- 内容: Claude Code の Dynamic Workflow / モデル（Opus・Sonnet・Haiku・Fable）の使い分け / 工数(effort)・Ultracode の解説。Anthropic 一次ドキュメントに基づく一般公開情報。
- 検閲結果: 会社名・取引先名・固有プロジェクト名・部署名・個人情報・秘密値なし。記載は公開モデルID・公開価格・公開ドキュメントURLのみ。**問題なし。**
- 検索除外: `<head>` に `noindex, nofollow` / `googlebot noindex, nofollow` メタを維持。

---

## 2026-06-26

### notes/ig-ai-shortvideo-playbook.html
- 内容: Instagram向け「AI業務活用」ショート動画の企画プレイブック。海外IG/Xトレンド発のネタ表と、他ジャンル由来33フォーマット（撮影/編集工数・優先度・参考動画埋め込み）。検証済みリサーチに基づく一般公開情報。
- 検閲結果: 会社名・取引先名・固有プロジェクト名・部署名・個人の連絡先・秘密値なし。記載は公開SNSクリエイターのハンドル／公開動画URL／公開記事URLのみ（いずれも公開情報）。**問題なし。**
- 参考動画URL: YouTubeはoEmbedで実在確認済、TikTok/Instagramは個別動画URL形式で部分確認（ページ内に「確認済/部分」ラベルを明示）。
- 検索除外: `<head>` に `noindex, nofollow` / `googlebot noindex, nofollow` メタを維持。動画はタップ時のみ外部埋め込みを読み込む（初期表示では外部リクエストを発生させない）。
