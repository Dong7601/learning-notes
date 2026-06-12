#!/usr/bin/env python3
import argparse
import collections
import datetime as dt
import html
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ALLOWED_TYPES = {"x", "article"}
EXCLUDED_TYPES = {"memo", "prompt"}


class ClipError(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="Build the public clip feed HTML.")
    parser.add_argument("--src", required=True, help="Directory containing clip Markdown files.")
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parent.parent / "clips" / "index.html"),
        help="Output HTML path. Defaults to ../clips/index.html relative to this script.",
    )
    return parser.parse_args()


def strip_quotes(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ClipError("malformed_frontmatter")

    frontmatter = {}
    for raw in lines[1:end]:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if raw[:1].isspace() or stripped.startswith("- "):
            continue
        if ":" not in line:
            raise ClipError("malformed_frontmatter")
        key, value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise ClipError("malformed_frontmatter")
        frontmatter[key] = strip_quotes(value)

    return frontmatter, "\n".join(lines[end + 1 :]).lstrip("\n")


def first_h1(markdown):
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return ""


def section_content(markdown, heading):
    lines = markdown.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+" + re.escape(heading) + r"\s*$", line):
            start = i + 1
            break
    if start is None:
        return ""

    collected = []
    for line in lines[start:]:
        if re.match(r"^##\s+", line):
            break
        collected.append(line)
    return "\n".join(collected).strip()


def remove_private_paragraphs(text):
    paragraphs = re.split(r"\n\s*\n", text.strip())
    public = []
    for paragraph in paragraphs:
        normalized = paragraph.strip()
        if not normalized:
            continue
        if normalized.startswith("備考"):
            continue
        public.append(normalized)
    return public


def normalize_date(value):
    if not value:
        return ""
    match = re.search(r"\d{4}-\d{2}-\d{2}", value)
    return match.group(0) if match else value[:10]


def month_label(date_value):
    try:
        parsed = dt.date.fromisoformat(date_value)
    except ValueError:
        return "日付未設定"
    return f"{parsed.year}年{parsed.month}月"


def normalize_source_url(url, clip_type):
    parsed = urlsplit(url.strip())
    if clip_type != "x" and parsed.netloc.lower() not in {"x.com", "twitter.com", "www.x.com", "www.twitter.com"}:
        return url.strip()

    filtered = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        lower = key.lower()
        if lower in {"s", "t", "ref", "ref_src", "source"} or lower.startswith("utm_"):
            continue
        filtered.append((key, value))
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(filtered), ""))


def classify_clip(frontmatter):
    source = frontmatter.get("source", "").strip()
    if not source.lower().startswith("http"):
        return None, "missing_or_private_source"

    raw_type = frontmatter.get("type", "").strip().lower()
    if raw_type in EXCLUDED_TYPES:
        return None, f"excluded_type_{raw_type}"
    if raw_type in ALLOWED_TYPES:
        return raw_type, ""
    if not raw_type and frontmatter.get("title") and source:
        return "article", ""
    return None, "unsupported_type"


def read_clip(path):
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8")

    frontmatter, markdown = parse_frontmatter(text)
    clip_type, reason = classify_clip(frontmatter)
    if reason:
        raise ClipError(reason)

    title = first_h1(markdown) or frontmatter.get("title", "").strip() or path.stem
    content = section_content(markdown, "内容メモ") or frontmatter.get("description", "").strip()
    paragraphs = remove_private_paragraphs(content)
    date_value = normalize_date(
        frontmatter.get("captured", "") or frontmatter.get("published", "") or frontmatter.get("created", "")
    )
    source = normalize_source_url(frontmatter.get("source", ""), clip_type)

    return {
        "title": title,
        "paragraphs": paragraphs,
        "date": date_value,
        "type": clip_type,
        "source": source,
        "filename": path.name,
        "month": month_label(date_value),
    }


def esc(value):
    return html.escape(value, quote=True)


def render_paragraphs(paragraphs):
    if not paragraphs:
        return '<p class="clip-body-empty">本文メモはありません。</p>'
    rendered = []
    for paragraph in paragraphs:
        lines = [esc(line.strip()) for line in paragraph.splitlines()]
        rendered.append("<p>" + "<br>".join(lines) + "</p>")
    return "\n".join(rendered)


def render_clip(clip):
    type_label = "X投稿" if clip["type"] == "x" else "記事"
    search_text = " ".join([clip["title"], " ".join(clip["paragraphs"])])
    return f"""        <article class="clip-card" data-type="{esc(clip['type'])}" data-search="{esc(search_text.lower())}">
          <div class="clip-meta">
            <time>{esc(clip['date'] or '日付未設定')}</time>
            <span class="clip-badge">{esc(type_label)}</span>
          </div>
          <h2>{esc(clip['title'])}</h2>
          <div class="clip-body">
{render_paragraphs(clip['paragraphs'])}
          </div>
          <a class="source-link" href="{esc(clip['source'])}" target="_blank" rel="noopener">元記事を開く →</a>
        </article>"""


def render_html(clips):
    grouped = collections.OrderedDict()
    for clip in clips:
        grouped.setdefault(clip["month"], []).append(clip)

    sections = []
    for month, items in grouped.items():
        cards = "\n".join(render_clip(item) for item in items)
        sections.append(
            f"""      <section class="month-section" data-month="{esc(month)}">
        <h2 class="month-title">{esc(month)}</h2>
{cards}
      </section>"""
        )

    body = "\n".join(sections) if sections else '      <p class="empty">掲載できるクリップはありません。</p>'
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="googlebot" content="noindex, nofollow">
  <title>クリップフィード — 学習ノート</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0b0f14;
      --panel: #111821;
      --panel-2: #162231;
      --text: #eef4fb;
      --muted: #a8b6c8;
      --line: #2b3a4b;
      --accent: #58d6c2;
      --accent-2: #f2c94c;
      --shadow: rgba(0, 0, 0, 0.35);
      --max: 980px;
    }}

    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(88, 214, 194, 0.12), transparent 34rem),
        linear-gradient(180deg, #0b0f14 0%, #101721 46%, #0b0f14 100%);
      color: var(--text);
      font-family: "Yu Gothic UI", "Meiryo", "Hiragino Kaku Gothic ProN", system-ui, sans-serif;
      line-height: 1.75;
    }}
    a {{ color: var(--accent); }}
    header, main, footer {{
      width: min(100% - 2rem, var(--max));
      margin: 0 auto;
    }}
    .hero {{ padding: 2.2rem 0 1.4rem; }}
    .back-link {{
      display: inline-flex;
      margin-bottom: 1rem;
      color: var(--accent);
      font-weight: 700;
      text-decoration: none;
    }}
    .back-link:hover {{ text-decoration: underline; }}
    .eyebrow {{
      margin: 0 0 0.6rem;
      color: var(--accent);
      font-size: 0.92rem;
      font-weight: 700;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(2rem, 5vw, 3.2rem);
      line-height: 1.2;
    }}
    .hero-summary {{
      max-width: 720px;
      margin: 1rem 0 0;
      color: var(--muted);
      font-size: clamp(1rem, 2vw, 1.12rem);
    }}
    .search-wrap {{
      position: sticky;
      top: 0;
      z-index: 5;
      padding: 1.2rem 0;
      margin-top: 0.5rem;
      background: linear-gradient(180deg, rgba(11,15,20,0.96) 60%, rgba(11,15,20,0));
    }}
    .search-box {{
      width: 100%;
      min-height: 3.2rem;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: var(--panel);
      color: var(--text);
      font: inherit;
      padding: 0.8rem 1rem;
    }}
    .search-box:focus-visible, .type-chip:focus-visible, .source-link:focus-visible, .back-link:focus-visible {{
      outline: 3px solid var(--accent-2);
      outline-offset: 2px;
    }}
    .type-filter {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 0.85rem;
    }}
    .type-chip {{
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(17, 24, 33, 0.78);
      color: var(--muted);
      font: inherit;
      font-size: 0.88rem;
      line-height: 1;
      padding: 0.55rem 0.85rem;
      cursor: pointer;
    }}
    .type-chip[aria-pressed="true"] {{
      border-color: var(--accent);
      color: var(--text);
      box-shadow: 0 0 0 2px rgba(88, 214, 194, 0.16);
    }}
    .count {{
      margin: 0.6rem 0 0;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .month-section {{ margin: 0 0 2.2rem; }}
    .month-section[hidden], .clip-card[hidden] {{ display: none; }}
    .month-title {{
      margin: 1.2rem 0 0.8rem;
      color: var(--text);
      font-size: 1.2rem;
      line-height: 1.35;
    }}
    .clip-card {{
      margin: 0 0 1rem;
      padding: 1.25rem 1.3rem;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: linear-gradient(180deg, rgba(22, 34, 49, 0.9), rgba(17, 24, 33, 0.9));
      box-shadow: 0 12px 30px var(--shadow);
    }}
    .clip-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      align-items: center;
      margin-bottom: 0.6rem;
      color: var(--muted);
      font-size: 0.85rem;
    }}
    .clip-badge {{
      display: inline-flex;
      align-items: center;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 0.18rem 0.65rem;
      background: rgba(17, 24, 33, 0.58);
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 700;
      line-height: 1.45;
    }}
    .clip-card h2 {{
      margin: 0 0 0.75rem;
      color: var(--text);
      font-size: 1.22rem;
      line-height: 1.35;
    }}
    .clip-body p {{
      margin: 0 0 0.8rem;
      color: var(--muted);
      font-size: 0.98rem;
    }}
    .clip-body-empty {{ color: var(--muted); }}
    .source-link {{
      display: inline-flex;
      margin-top: 0.2rem;
      font-weight: 700;
      text-decoration: none;
    }}
    .source-link:hover {{ text-decoration: underline; }}
    .empty {{
      padding: 2rem 1rem;
      text-align: center;
      color: var(--muted);
      border: 1px dashed var(--line);
      border-radius: 12px;
    }}
    footer {{
      padding: 2.5rem 0 3.5rem;
      color: var(--muted);
      border-top: 1px solid rgba(168, 182, 200, 0.14);
      font-size: 0.9rem;
    }}
    footer p {{ margin: 0.3rem 0; }}
  </style>
</head>
<body>
  <header class="hero">
    <a class="back-link" href="../index.html">← 学習ノート一覧へ戻る</a>
    <p class="eyebrow">External clips</p>
    <h1>クリップフィード</h1>
    <p class="hero-summary">外部記事とX投稿から、後で読み返したい公開メモだけをまとめたフィード。<span id="total-count">{len(clips)}</span>件掲載。</p>
  </header>

  <main>
    <div class="search-wrap">
      <input id="search" class="search-box" type="search" placeholder="キーワードで検索" aria-label="クリップを検索" autocomplete="off">
      <div class="type-filter" id="type-filter" aria-label="種別で絞り込み"></div>
      <p class="count" id="count"></p>
    </div>

    <div id="clip-list">
{body}
    </div>
  </main>

  <footer>
    <p>検索エンジン除外設定済み。公開URLと公開向け要約のみを掲載しています。</p>
  </footer>

  <script>
    var TYPE_LABELS = {{
      all: "すべて",
      x: "X投稿",
      article: "記事"
    }};
    var activeType = "all";
    var searchEl = document.getElementById("search");
    var typeFilterEl = document.getElementById("type-filter");
    var countEl = document.getElementById("count");
    var cards = Array.prototype.slice.call(document.querySelectorAll(".clip-card"));
    var sections = Array.prototype.slice.call(document.querySelectorAll(".month-section"));

    function escapeHtml(s) {{
      return s.replace(/[&<>"']/g, function (c) {{
        return {{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }}[c];
      }});
    }}

    function renderTypeChips() {{
      typeFilterEl.innerHTML = ["all", "x", "article"].map(function (type) {{
        return '<button class="type-chip" type="button" data-type="' + type + '" aria-pressed="' + (activeType === type ? "true" : "false") + '">' + escapeHtml(TYPE_LABELS[type]) + '</button>';
      }}).join("");
    }}

    function cardMatches(card, terms) {{
      if (activeType !== "all" && card.getAttribute("data-type") !== activeType) return false;
      if (!terms.length) return true;
      var hay = card.getAttribute("data-search") || "";
      return terms.every(function (term) {{ return hay.indexOf(term) !== -1; }});
    }}

    function render() {{
      var query = searchEl.value.trim().toLowerCase();
      var terms = query ? query.split(/\\s+/) : [];
      var matched = 0;

      cards.forEach(function (card) {{
        var visible = cardMatches(card, terms);
        card.hidden = !visible;
        if (visible) matched += 1;
      }});

      sections.forEach(function (section) {{
        var visibleCards = section.querySelectorAll(".clip-card:not([hidden])");
        section.hidden = visibleCards.length === 0;
      }});

      countEl.textContent = query || activeType !== "all"
        ? matched + " 件ヒット（全 " + cards.length + " 件）"
        : matched + " 件表示（全 " + cards.length + " 件）";
    }}

    typeFilterEl.addEventListener("click", function (event) {{
      var button = event.target.closest("[data-type]");
      if (!button) return;
      activeType = button.getAttribute("data-type");
      renderTypeChips();
      render();
    }});
    searchEl.addEventListener("input", render);
    renderTypeChips();
    render();
  </script>
</body>
</html>
"""


def build(src, out):
    clips = []
    excluded = collections.Counter()

    for path in sorted(src.glob("*.md"), key=lambda p: p.name):
        try:
            clips.append(read_clip(path))
        except ClipError as exc:
            excluded[str(exc)] += 1
        except OSError:
            excluded["read_error"] += 1

    clips.sort(key=lambda clip: (clip["date"], clip["filename"]), reverse=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_html(clips), encoding="utf-8", newline="\n")
    return clips, excluded


def main():
    args = parse_args()
    src = Path(args.src)
    out = Path(args.out)
    if not src.is_dir():
        print("error: --src must be a directory", file=sys.stderr)
        return 2

    clips, excluded = build(src, out)
    reasons = ", ".join(f"{reason}: {count}" for reason, count in sorted(excluded.items()))
    if not reasons:
        reasons = "なし"
    print(f"掲載{len(clips)}件 / 除外{sum(excluded.values())}件({reasons})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
