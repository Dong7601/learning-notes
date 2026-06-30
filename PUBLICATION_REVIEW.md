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


### notes/ai-shortvideo-shooting-templates.html
- 内容: AI業務活用ショート動画の共通フォーマット撮影テンプレ（絵コンテ＋台本＋ネタバンク）。日本型フォーマット調査の派生。
- 検閲結果: 会社名・取引先名・固有プロジェクト名・部署名・個人連絡先・秘密値なし。公開クリエイターの公開動画URL（YouTube oEmbed確認済）と一般的な制作手順のみ。台本内に「画面に社名・本文・個人情報を映さない／数値は実測」の注意を明記。**問題なし。**
- 検索除外: `<head>` に `noindex, nofollow` / `googlebot noindex, nofollow` メタを維持。

---

## 2026-06-28

### notes/iphone-x-usage-gate-scriptable.html
- 内容: Mac無しでiPhoneのX開きすぎを抑止する個人用ツール（iOSショートカット自動化＋Scriptable/JavaScript＋WebView）の実装と仕組み・ハマりどころ。本人の実体験ベースの技術解説。
- 検閲結果: 会社名・取引先名・固有プロジェクト名・部署名・個人情報・連絡先・秘密値・トークン類なし。本人の利用習慣は「本人用」と匿名化、固有名はアプリ名(Scriptable/one sec)とOS機能名・公開URLスキームのみ。**問題なし。**
- 検索除外: `<head>` に `noindex, nofollow` / `googlebot noindex, nofollow` メタを維持。

---

## 2026-06-30

### notes/consultant-slide-best-practices.html ＋ notes/assets/consultant-slide-bp/*.png
- 内容: コンサル／官公庁向け調査報告デッキの観察から抽出した、スライドのメッセージ・デザインの普遍原則（タイトル＝結論、3階調カード、対立、試算の段階分解、配色・出典の規律、デッキ構成テンプレ等）。一般教育内容。
- **検閲結果: 問題なし。** 会社名・取引先名・固有プロジェクト名・部署名・個人名（情報源の人名を含む）・連絡先・秘密値なし。特定の委託調査名や内部共有フォルダ名は記載していない。
- **画像: 実在資料は一切転載していない。** 埋め込み画像6点は本ツール(regrit-style-deck)で生成した**ブランド中立の自作サンプルスライド**（ブランド名は "Sample"、内容は架空の一般例）。各図のキャプションと脚注に「自作サンプル／実在資料の転載ではない」と明記。
- 各社の作風への言及は「実務ナビ型／論証・厳密型」という一般論の対比に留め、固有の社名・資料名は出していない。
- 検索除外: `<head>` に `noindex, nofollow` / `googlebot noindex, nofollow` メタを維持。
