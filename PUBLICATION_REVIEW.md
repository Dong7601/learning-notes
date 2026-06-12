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

### 検索除外
- robots.txt に `Disallow: /` を設置。
- 全HTMLの `<head>` に `noindex, nofollow` メタを設置。
- notes/_template.html：ひな型（プレースホルダのみ・機密情報なし）
