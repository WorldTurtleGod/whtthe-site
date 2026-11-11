#!/usr/bin/env python3
"""Turn article text files into pages for What The? News.

This script only writes files under the site folder. It does not
publish, push, or talk to GitHub.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from calendar import day_name
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_source" / "editions"
TEMPLATES = Path(__file__).resolve().parent / "templates"
SITE_URL = "https://www.whtthe.com"
# Site color theme: "green" (turtle / pale sage) or "blue" (ocean / pale sky).
# Change this one value to set the default after a color is chosen.
# Keep the CSS fallback in css/style.css in sync (the :root, [data-theme="..."] rule).
DEFAULT_THEME = "blue"
DEFAULT_SHARE_IMAGE = f"{SITE_URL}/images/share-default.png"
ARCHIVE_PAGE_SIZE = 8  # editions per archive page
SECTION_PAGE_SIZE = 12  # articles per desk or author page

DESKS = {
    "games": ("Games", "games"),
    "power": ("Power", "power"),
    "tech & ai": ("Tech & AI", "tech"),
    "tech and ai": ("Tech & AI", "tech"),
    "tech": ("Tech & AI", "tech"),
    "culture": ("Culture", "culture"),
    "science": ("Science", "science"),
    "strange": ("Strange", "strange"),
}

DESK_ORDER = [
    ("games", "Games"),
    ("power", "Power"),
    ("tech", "Tech & AI"),
    ("culture", "Culture"),
    ("science", "Science"),
    ("strange", "Strange"),
]

NAV_ITEMS = [
    ("home", "Home", "/"),
    ("games", "Games", "/games/"),
    ("power", "Power", "/power/"),
    ("tech", "Tech & AI", "/tech/"),
    ("culture", "Culture", "/culture/"),
    ("science", "Science", "/science/"),
    ("strange", "Strange", "/strange/"),
    ("archive", "Archive", "/archive/"),
    ("about", "About", "/about/"),
]

RESERVED_AUTHORS = {
    "staff",
    "the staff",
    "editor",
    "editors",
    "admin",
    "anonymous",
    "author",
}

GENERATED_DIRS = {
    "games",
    "power",
    "tech",
    "culture",
    "science",
    "strange",
    "authors",
    "archive",
    "about",
}

CURRENT = ' aria-current="page"'
WARNINGS: list[str] = []


def warn(message: str) -> None:
    WARNINGS.append(message)
    print(f"Warning: {message}", file=sys.stderr)


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def edition_pad(num: int) -> str:
    return f"{num:03d}"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "story"


def parse_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text.strip()
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text.strip()
    meta: dict[str, str] = {}
    for raw in parts[1].splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip().strip('"').strip("'")
    return meta, parts[2].strip()


def format_date(value: date) -> str:
    return f"{day_name[value.weekday()]}, {value.strftime('%B')} {value.day}, {value.year}"


def format_short_date(value: date) -> str:
    return f"{value.strftime('%b')} {value.day}, {value.year}"


def parse_date(value: str, label: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        fail(f"{label} must look like 2026-11-10 (year-month-day). Got: {value}")


def load_template(name: str) -> str:
    path = TEMPLATES / name
    if not path.is_file():
        fail(f"Missing template: {path}")
    return path.read_text(encoding="utf-8")


def fill(template: str, mapping: dict[str, str]) -> str:
    out = template
    for key, value in mapping.items():
        out = out.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{[A-Z0-9_]+\}\}", out)
    if leftover:
        fail(f"Template still has unfilled placeholders: {', '.join(leftover)}")
    return out


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def abs_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return SITE_URL + path


def normalize_desk(raw: str) -> tuple[str, str]:
    key = raw.strip().lower()
    if key not in DESKS:
        allowed = "Games, Power, Tech & AI, Culture, Science, Strange"
        fail(f'Unknown desk "{raw}". Use one of: {allowed}.')
    return DESKS[key]


def inline_format(text: str) -> str:
    pieces: list[str] = []
    pos = 0
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for match in pattern.finditer(text):
        pieces.append(_marks(text[pos:match.start()]))
        label = _marks(match.group(1))
        href = esc(match.group(2))
        pieces.append(f'<a href="{href}">{label}</a>')
        pos = match.end()
    pieces.append(_marks(text[pos:]))
    return "".join(pieces)


def _marks(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", lambda m: "<code>" + m.group(1) + "</code>", escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped


def render_body(text: str, sources: list[Source]) -> str:
    blocks = re.split(r"\n\s*\n", text.strip())
    html_blocks: list[str] = []
    for block in blocks:
        stripped = block.strip()
        if not stripped:
            continue
        if stripped.startswith("## "):
            html_blocks.append("<h2>" + inline_format(stripped[3:].strip()) + "</h2>")
            continue
        if stripped.startswith("# "):
            html_blocks.append("<h2>" + inline_format(stripped[2:].strip()) + "</h2>")
            continue
        if all(line.strip().startswith(("- ", "* ")) for line in stripped.splitlines()):
            items = []
            for line in stripped.splitlines():
                items.append("<li>" + inline_format(line.strip()[2:].strip()) + "</li>")
            html_blocks.append("<ul>" + "".join(items) + "</ul>")
            continue
        html_blocks.append("<p>" + inline_format(stripped.replace("\n", " ")) + "</p>")
    return link_citations("\n".join(html_blocks), sources)


def link_citations(text: str, sources: list[Source]) -> str:
    known = {str(s.number) for s in sources}
    if not known:
        return text
    seen: set[str] = set()

    def repl(match: re.Match) -> str:
        number = match.group(1)
        if number not in known:
            return match.group(0)
        ident = f' id="cite-{number}"' if number not in seen else ""
        seen.add(number)
        return f'<a class="cite" href="#source-{number}"{ident}>[{number}]</a>'

    return re.sub(r"\[(\d+)\](?!\()", repl, text)


def collect_citations(text: str) -> list[int]:
    found = [int(n) for n in re.findall(r"\[(\d+)\](?!\()", text)]
    # unique, keep order
    out: list[int] = []
    for n in found:
        if n not in out:
            out.append(n)
    return out


class Source:
    def __init__(self, number: int, title: str, outlet: str, url: str, note: str):
        self.number = number
        self.title = title
        self.outlet = outlet
        self.url = url
        self.note = note


class Evidence:
    def __init__(self, kind: str, text: str, extra: str = ""):
        self.kind = kind  # quote, image, document
        self.text = text
        self.extra = extra


def parse_body_sections(text: str) -> tuple[str, list[Source], list[Evidence]]:
    body_lines: list[str] = []
    source_lines: list[str] = []
    evidence_lines: list[str] = []
    mode = "body"
    for line in text.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"sources:\s*", stripped, re.I):
            mode = "sources"
            continue
        if re.fullmatch(r"evidence:\s*", stripped, re.I):
            mode = "evidence"
            continue
        if mode == "body":
            body_lines.append(line)
        elif mode == "sources":
            source_lines.append(line)
        else:
            evidence_lines.append(line)
    return (
        "\n".join(body_lines).strip(),
        parse_sources(source_lines),
        parse_evidence(evidence_lines),
    )


def parse_sources(lines: list[str]) -> list[Source]:
    sources: list[Source] = []
    auto = 1
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        number = auto
        numbered = re.match(r"^(\d+)[.)]\s+", line)
        if numbered:
            number = int(numbered.group(1))
            line = line[numbered.end() :]
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3 or not parts[0] or not parts[2]:
            warn(
                f"Skipped a source line that was missing a title or a URL: {raw.strip()}"
            )
            continue
        title, outlet, url = parts[0], parts[1], parts[2]
        note = parts[3] if len(parts) > 3 else ""
        sources.append(Source(number, title, outlet, url, note))
        auto = number + 1
    return sources


def parse_evidence(lines: list[str]) -> list[Evidence]:
    items: list[Evidence] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        if ":" not in line:
            warn(f"Skipped an evidence line that had no type (quote, image, or document): {raw.strip()}")
            continue
        kind, rest = line.split(":", 1)
        kind = kind.strip().lower()
        rest = rest.strip()
        if kind not in {"quote", "image", "document"}:
            warn(f'Skipped evidence with unknown type "{kind}". Use quote, image, or document.')
            continue
        if kind == "quote":
            text, attr = split_quote(rest)
            items.append(Evidence("quote", text, attr))
        else:
            parts = [p.strip() for p in rest.split("|", 1)]
            target = parts[0]
            label = parts[1] if len(parts) > 1 else ""
            if not target:
                warn(f"Skipped a {kind} evidence item that was missing a path or URL.")
                continue
            items.append(Evidence(kind, target, label))
    return items


def split_quote(text: str) -> tuple[str, str]:
    for sep in (" — ", " -- ", " —", " – "):
        if sep in text:
            left, right = text.rsplit(sep, 1)
            return left.strip().strip('"'), right.strip()
    return text.strip().strip('"'), ""


class Article:
    def __init__(self, path: Path, edition: int, edition_date: date):
        meta, raw_body = parse_frontmatter(path.read_text(encoding="utf-8"))
        title = meta.get("title", "").strip()
        desk_raw = meta.get("desk", "").strip()
        author = meta.get("author", "").strip()
        if not title:
            fail(f"{path.name} needs a title in the header.")
        if not desk_raw:
            fail(f"{path.name} needs a desk in the header.")
        if not author:
            if meta.get("byline", "").strip():
                fail(
                    f"{path.name} uses a byline field. Put the writer's name in an author field instead, like: author: Juno"
                )
            fail(
                f"{path.name} needs an author in the header, like: author: Juno. "
                "Use the writer's name. Do not use Staff."
            )
        if author.lower() in RESERVED_AUTHORS:
            fail(
                f'{path.name} must use the writer\'s actual name, not "{author}". '
                "A generic label like Staff is not allowed."
            )
        self.title = title
        self.desk, self.desk_class = normalize_desk(desk_raw)
        self.dek = meta.get("dek", "").strip()
        self.author = author
        self.author_slug = slugify(author)
        self.slug = slugify(meta.get("slug") or path.stem)
        self.lead = parse_bool(meta.get("lead"))
        self.sample = parse_bool(meta.get("sample"))
        self.image = meta.get("image", "").strip()
        self.edition = edition
        self.date = edition_date
        if meta.get("date"):
            self.date = parse_date(meta["date"], f"Date in {path.name}")
        body, sources, evidence = parse_body_sections(raw_body)
        self.sources = sources
        self.evidence = evidence
        self.body_text = body
        self.citations = collect_citations(body)
        self.body_html = render_body(body, sources)
        self.source_path = path
        self._check_sources()

    def _check_sources(self) -> None:
        label = f"{self.source_path.name} (Edition {self.edition})"
        if not self.sources:
            warn(f"{label} has no Sources list. The story will still be built, but the Sources & Evidence section will be left off.")
        known = {s.number for s in self.sources}
        for number in self.citations:
            if number not in known:
                warn(f"{label} cites [{number}], but there is no source with that number.")

    def path(self) -> str:
        d = self.date
        return f"/{d.year}/{d.month:02d}/{d.day:02d}/{self.slug}/"

    def url(self) -> str:
        return SITE_URL + self.path()

    def author_path(self) -> str:
        return f"/authors/{self.author_slug}/"

    def desk_path(self) -> str:
        return f"/{self.desk_class}/"

    def share_image(self) -> str:
        if self.image:
            return abs_url(self.image)
        return DEFAULT_SHARE_IMAGE

    def sample_badge(self) -> str:
        if not self.sample:
            return ""
        return '<span class="sample-badge">Sample article</span>'

    def dek_block(self, class_name: str = "dek") -> str:
        if not self.dek:
            return ""
        return f'<p class="{class_name}">{html.escape(self.dek)}</p>'

    def byline_link(self) -> str:
        return f'<a href="{esc(self.author_path())}">{html.escape(self.author)}</a>'

    def date_iso(self) -> str:
        return self.date.isoformat()


def sort_articles(articles: list[Article]) -> list[Article]:
    # Newest date first, then higher edition, lead story first, then title A-Z.
    return sorted(
        articles,
        key=lambda a: (-a.date.toordinal(), -a.edition, 0 if a.lead else 1, a.title.lower()),
    )


def read_meta(folder: Path) -> dict:
    path = folder / "meta.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Could not read {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path} should be a small settings file with a date and a lead story.")
    return data


def list_article_files(folder: Path) -> list[Path]:
    files = sorted(
        p for p in folder.iterdir() if p.suffix.lower() in {".md", ".txt"} and p.is_file()
    )
    if not files:
        fail(f"No article files (.md or .txt) found in {folder}")
    return files


def load_edition(
    num: int, date_override: str | None = None, files: list[Path] | None = None
) -> tuple[date, list[Article]]:
    folder = SOURCE / edition_pad(num)
    meta = read_meta(folder) if folder.is_dir() else {}
    if date_override:
        edition_date = parse_date(date_override, "The --date value")
    elif meta.get("date"):
        edition_date = parse_date(str(meta["date"]), f"Date in {folder / 'meta.json'}")
    else:
        fail(
            f"Edition {edition_pad(num)} needs a date. Pass --date 2026-11-10 "
            "or add one in _source/editions/" + edition_pad(num) + "/meta.json."
        )

    if files:
        paths = files
    else:
        if not folder.is_dir():
            fail(f"Could not find article folder: {folder}")
        paths = list_article_files(folder)

    articles = [Article(path, num, edition_date) for path in paths]
    lead_slug = meta.get("lead")
    if lead_slug:
        found = False
        for article in articles:
            if article.slug == lead_slug:
                article.lead = True
                found = True
            else:
                article.lead = False
        if not found:
            fail(f'meta.json names lead "{lead_slug}", but no article has that slug.')
    if not any(a.lead for a in articles):
        articles[0].lead = True
    if sum(1 for a in articles if a.lead) > 1:
        seen = False
        for article in articles:
            if article.lead and not seen:
                seen = True
            else:
                article.lead = False
    return edition_date, articles


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def clean_generated() -> None:
    for name in GENERATED_DIRS:
        path = ROOT / name
        if path.is_dir():
            shutil.rmtree(path)
    for path in list(ROOT.iterdir()):
        if path.is_dir() and re.fullmatch(r"20\d{2}", path.name):
            shutil.rmtree(path)
    old_editions = ROOT / "editions"
    if old_editions.is_dir():
        shutil.rmtree(old_editions)
    for name in ("about.html", "archive.html", "404.html", "feed.xml", "sitemap.xml"):
        path = ROOT / name
        if path.is_file():
            path.unlink()


def nav_html(current: str) -> str:
    parts = []
    for key, label, href in NAV_ITEMS:
        current_attr = CURRENT if key == current else ""
        parts.append(f'<a href="{esc(href)}"{current_attr}>{html.escape(label)}</a>')
    return "\n      ".join(parts)


def page(
    *,
    title: str,
    description: str,
    canonical: str,
    current: str,
    content: str,
    og_type: str = "website",
    og_title: str | None = None,
    og_image: str = DEFAULT_SHARE_IMAGE,
    head_extra: str = "",
    scripts: str = "",
) -> str:
    return fill(
        load_template("base.html"),
        {
            "TITLE": esc(title),
            "DESCRIPTION": esc(description),
            "CANONICAL": esc(canonical),
            "OG_TITLE": esc(og_title or title),
            "OG_IMAGE": esc(og_image),
            "OG_TYPE": esc(og_type),
            "HEAD_EXTRA": head_extra,
            "NAV": nav_html(current),
            "CONTENT": content,
            "SCRIPTS": scripts,
            "THEME": DEFAULT_THEME,
        },
    )


def thumb(article: Article, label: str = "Story image coming later") -> str:
    return (
        f'<a class="thumb thumb-{article.desk_class}" href="{esc(article.path())}" tabindex="-1" aria-hidden="true">'
        f'<span class="thumb-mark">?</span>'
        f'<span class="thumb-desk">{html.escape(article.desk)}</span>'
        f'<span class="sr-only">Placeholder image</span>'
        f"</a>"
    )


def kicker_html(article: Article) -> str:
    desk = (
        f'<a class="desk desk-{article.desk_class}" href="{esc(article.desk_path())}">'
        f"{html.escape(article.desk)}</a>"
    )
    return f'<p class="kicker">{desk} {article.sample_badge()}</p>'


def meta_line(article: Article, class_name: str = "card-meta") -> str:
    return (
        f'<p class="{class_name}">By {article.byline_link()}'
        f'<span class="sep" aria-hidden="true">·</span>'
        f'<time datetime="{article.date_iso()}">{format_short_date(article.date)}</time>'
        f'<span class="sep" aria-hidden="true">·</span>'
        f"Edition {article.edition}</p>"
    )


def card_html(article: Article) -> str:
    return (
        '<article class="card">\n'
        f"  {thumb(article)}\n"
        f"  {kicker_html(article)}\n"
        f'  <h2 class="headline"><a href="{esc(article.path())}">{html.escape(article.title)}</a></h2>\n'
        f"  {article.dek_block()}\n"
        f"  {meta_line(article)}\n"
        "</article>\n"
    )


def story_row_html(article: Article) -> str:
    return (
        '<article class="story-row">\n'
        f"  {thumb(article)}\n"
        "  <div>\n"
        f"    {kicker_html(article)}\n"
        f'    <h2 class="headline"><a href="{esc(article.path())}">{html.escape(article.title)}</a></h2>\n'
        f"    {article.dek_block()}\n"
        f"    {meta_line(article)}\n"
        "  </div>\n"
        "</article>\n"
    )


def tease_html(article: Article) -> str:
    return (
        '<article class="tease">\n'
        f"  {kicker_html(article)}\n"
        f'  <h3 class="headline"><a href="{esc(article.path())}">{html.escape(article.title)}</a></h3>\n'
        f"  {article.dek_block()}\n"
        f"  {meta_line(article)}\n"
        "</article>\n"
    )


def pager_html(prev_href: str | None, next_href: str | None, label: str) -> str:
    if not prev_href and not next_href:
        return ""
    parts = ['<nav class="pager" aria-label="More pages">']
    if prev_href:
        parts.append(f'<a href="{esc(prev_href)}" rel="prev">Previous {label}</a>')
    if next_href:
        parts.append(f'<a href="{esc(next_href)}" rel="next">More {label}</a>')
    parts.append("</nav>")
    return "\n".join(parts)


def chunks(items: list, size: int) -> list[list]:
    if not items:
        return [[]]
    return [items[i : i + size] for i in range(0, len(items), size)]


def share_bar(article: Article, extra_class: str = "") -> str:
    url = article.url()
    title = article.title
    q_url = quote(url, safe="")
    q_title = quote(title, safe="")
    x_href = f"https://x.com/intent/post?text={q_title}&url={q_url}"
    fb_href = f"https://www.facebook.com/sharer/sharer.php?u={q_url}"
    reddit_href = f"https://www.reddit.com/submit?url={q_url}&title={q_title}"
    body = quote(f"{title}\n{url}", safe="")
    email_href = f"mailto:?subject={q_title}&body={body}"
    cls = "share-bar" + (f" {extra_class}" if extra_class else "")
    return f'''<div class="{cls}" data-share-url="{esc(url)}" data-share-title="{esc(title)}">
  <p class="share-label">Share</p>
  <div class="share-actions">
    <button type="button" class="share-btn" data-copy-link>Copy link</button>
    <span class="share-copied" hidden>Copied</span>
    <a class="share-btn" href="{esc(x_href)}" target="_blank" rel="noopener noreferrer">Share on X</a>
    <a class="share-btn" href="{esc(fb_href)}" target="_blank" rel="noopener noreferrer">Facebook</a>
    <a class="share-btn" href="{esc(reddit_href)}" target="_blank" rel="noopener noreferrer">Reddit</a>
    <a class="share-btn" href="{esc(email_href)}">Email</a>
    <button type="button" class="share-btn share-native" hidden>Share</button>
  </div>
</div>'''


def sources_section(article: Article) -> str:
    if not article.sources and not article.evidence:
        return ""
    parts = ['<section class="sources-block" id="sources" aria-labelledby="sources-heading">']
    parts.append('<h2 id="sources-heading">Sources &amp; Evidence</h2>')
    if article.sources:
        parts.append('<ol class="sources-list">')
        for source in article.sources:
            note = (
                f'<p class="source-note">{html.escape(source.note)}</p>'
                if source.note
                else ""
            )
            outlet = (
                f'<span class="source-outlet">{html.escape(source.outlet)}</span>'
                if source.outlet
                else ""
            )
            parts.append(
                f'<li id="source-{source.number}">'
                f'<a class="source-title" href="{esc(source.url)}" target="_blank" rel="noopener noreferrer">'
                f"{html.escape(source.title)}</a>"
                f"{outlet}{note}</li>"
            )
        parts.append("</ol>")
    if article.evidence:
        parts.append('<div class="evidence-list">')
        for item in article.evidence:
            if item.kind == "quote":
                footer = f"<footer>{html.escape(item.extra)}</footer>" if item.extra else ""
                parts.append(
                    f"<blockquote class=\"evidence-quote\"><p>{html.escape(item.text)}</p>{footer}</blockquote>"
                )
            elif item.kind == "image":
                src = item.text if item.text.startswith(("http://", "https://", "/")) else "/" + item.text
                caption = item.extra or "Evidence image"
                parts.append(
                    "<figure class=\"evidence-figure\">"
                    f'<img src="{esc(src)}" alt="{esc(caption)}">'
                    f"<figcaption>{html.escape(caption)}</figcaption>"
                    "</figure>"
                )
            elif item.kind == "document":
                label = item.extra or item.text
                href = item.text
                parts.append(
                    f'<p class="evidence-doc">Document: '
                    f'<a href="{esc(href)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a></p>'
                )
        parts.append("</div>")
    parts.append("</section>")
    return "\n".join(parts)


def build_article_page(article: Article, related: list[Article]) -> str:
    iso = article.date.isoformat()
    head_extra = "\n".join(
        [
            f'<meta property="article:author" content="{esc(article.author)}">',
            f'<meta property="article:published_time" content="{esc(iso)}">',
            f'<meta property="article:section" content="{esc(article.desk)}">',
        ]
    )
    more = ""
    others = [a for a in related if a.path() != article.path()][:4]
    if others:
        more = (
            '<aside class="article-more">'
            f'<h2 class="section-title">More from {html.escape(article.desk)}</h2>'
            + "".join(tease_html(a) for a in others)
            + "</aside>"
        )
    content = f'''<main id="main">
  <article>
    <header class="article-header">
      {kicker_html(article)}
      <h1 class="headline">{html.escape(article.title)}</h1>
      {article.dek_block()}
      <p class="byline">By {article.byline_link()}<span class="sep" aria-hidden="true">·</span><time datetime="{iso}">{format_date(article.date)}</time><span class="sep" aria-hidden="true">·</span>Edition {article.edition}</p>
    </header>
    <div class="share-wrap">
      {share_bar(article)}
    </div>
    <div class="article-body">
      {article.body_html}
    </div>
    {sources_section(article)}
    <div class="share-wrap">
      {share_bar(article, "share-bottom")}
    </div>
  </article>
  {more}
</main>'''
    scripts = '<script src="/js/share.js" defer></script>'
    desc = article.dek or article.title
    return page(
        title=f"{article.title} — What The? News",
        description=desc,
        canonical=article.url(),
        current=article.desk_class,
        content=content,
        og_type="article",
        og_title=article.title,
        og_image=article.share_image(),
        head_extra=head_extra,
        scripts=scripts,
    )


def build_index(num: int, edition_date: date, latest_articles: list[Article], all_articles: list[Article]) -> str:
    lead = next(a for a in latest_articles if a.lead)
    others = [a for a in latest_articles if not a.lead]
    rail_items = []
    for article in sort_articles(all_articles)[:10]:
        rail_items.append(
            "<li>"
            f'<div><a href="{esc(article.path())}">{html.escape(article.title)}</a>'
            f'<span class="rail-meta">{html.escape(article.desk)} · {format_short_date(article.date)}</span></div>'
            "</li>"
        )
    desks = []
    by_desk: dict[str, list[Article]] = defaultdict(list)
    for article in sort_articles(all_articles):
        by_desk[article.desk_class].append(article)
    for desk_class, desk_name in DESK_ORDER:
        stories = by_desk.get(desk_class, [])[:3]
        body = (
            "".join(tease_html(a) for a in stories)
            if stories
            else '<p class="empty-desk">No stories on this desk yet.</p>'
        )
        desks.append(
            f'<section class="desk-board" aria-labelledby="desk-{desk_class}">'
            f'<h2 class="section-title" id="desk-{desk_class}">'
            f'<a href="/{desk_class}/">{html.escape(desk_name)}</a>'
            f'<a class="more-link" href="/{desk_class}/">All {html.escape(desk_name)}</a>'
            f"</h2>{body}</section>"
        )
    content = f'''<main id="main" class="wrap">
  <div class="edition-line">
    <p class="edition-no">Edition {num}</p>
    <p class="edition-date">{format_date(edition_date)}</p>
  </div>
  <section class="home-hero" aria-label="Top story">
    <div class="hero-media">{thumb(lead, "Lead story image coming later")}</div>
    <div class="hero-copy">
      {kicker_html(lead)}
      <h1 class="headline"><a href="{esc(lead.path())}">{html.escape(lead.title)}</a></h1>
      {lead.dek_block()}
      {meta_line(lead, "hero-meta")}
    </div>
  </section>
  <div class="home-body">
    <section aria-labelledby="latest-heading">
      <h2 class="section-title" id="latest-heading">Latest in this edition</h2>
      <div class="latest-grid">
        {"".join(card_html(a) for a in others)}
      </div>
    </section>
    <aside class="latest-rail" aria-labelledby="rail-heading">
      <h2 class="section-title" id="rail-heading">Latest</h2>
      <ol>
        {"".join(rail_items)}
      </ol>
    </aside>
  </div>
  <div class="desk-boards">
    {"".join(desks)}
  </div>
</main>'''
    return page(
        title=f"What The? News — Edition {num}",
        description=f"Edition {num} of What The? News for {format_date(edition_date)}. A daily paper from WorldTurtleGod Studios.",
        canonical=f"{SITE_URL}/",
        current="home",
        content=content,
    )


def build_list_page(
    *,
    title: str,
    heading: str,
    intro: str,
    canonical_path: str,
    current: str,
    articles: list[Article],
    page_number: int,
    page_count: int,
    base_path: str,
) -> str:
    start = (page_number - 1) * SECTION_PAGE_SIZE
    slice_ = articles[start : start + SECTION_PAGE_SIZE]
    rows = "".join(story_row_html(a) for a in slice_) or '<p class="empty-desk">No stories here yet.</p>'
    prev_href = None
    next_href = None
    if page_number > 1:
        prev_href = base_path if page_number == 2 else f"{base_path}page/{page_number - 1}/"
    if page_number < page_count:
        next_href = f"{base_path}page/{page_number + 1}/"
    suffix = f" — Page {page_number}" if page_number > 1 else ""
    canonical = SITE_URL + (canonical_path if page_number == 1 else f"{base_path}page/{page_number}/")
    content = f'''<main id="main" class="wrap">
  <header class="page-header">
    <h1 class="page-title">{html.escape(heading)}</h1>
    <p class="page-intro">{html.escape(intro)}</p>
  </header>
  <div class="story-list">
    {rows}
  </div>
  {pager_html(prev_href, next_href, "stories")}
</main>'''
    return page(
        title=f"{title}{suffix} — What The? News" if not title.endswith("What The? News") else f"{heading}{suffix} — What The? News",
        description=intro,
        canonical=canonical,
        current=current,
        content=content,
    )


def write_paginated_list(
    *,
    heading: str,
    intro: str,
    current: str,
    articles: list[Article],
    base_dir: Path,
    base_path: str,
    title: str,
) -> None:
    pages = chunks(articles, SECTION_PAGE_SIZE)
    page_count = max(1, len(pages) if articles else 1)
    for i in range(page_count):
        number = i + 1
        html_page = build_list_page(
            title=title,
            heading=heading,
            intro=intro,
            canonical_path=base_path,
            current=current,
            articles=articles,
            page_number=number,
            page_count=page_count,
            base_path=base_path,
        )
        dest = base_dir / "index.html" if number == 1 else base_dir / "page" / str(number) / "index.html"
        write(dest, html_page)


def build_about() -> str:
    content = '''<main id="main" class="prose">
  <header class="page-header">
    <h1 class="page-title">About</h1>
  </header>
  <p>What The? News is a WorldTurtleGod Studios project. We publish a new edition every day, with short stories from six desks: Games, Power, Tech &amp; AI, Culture, Science, and Strange.</p>
  <p>Each story carries the writer's name — for example, By Juno or By Vesper — and that name links to a page of their work. Editions come from Juno and Vesper. The aim is simple: a daily paper you can actually finish, with a little wonder and a straight face — until the story no longer allows it.</p>
  <p>When a story leans on source material, the article page includes a Sources &amp; Evidence section, with links you can follow and, when needed, a quote, a picture, or a document. Every article also has a share bar, so you can copy a direct link or post the full story to X and elsewhere.</p>
  <h2>How desks are labeled</h2>
  <p>Each story carries a text label for its desk. The labels also use a different outline, so they stay distinct even if color is hard to see:</p>
  <ul class="desk-key">
    <li><span class="desk desk-games">Games</span> solid square outline</li>
    <li><span class="desk desk-power">Power</span> double outline</li>
    <li><span class="desk desk-tech">Tech &amp; AI</span> dashed outline</li>
    <li><span class="desk desk-culture">Culture</span> dotted outline</li>
    <li><span class="desk desk-science">Science</span> solid outline with a drop shadow</li>
    <li><span class="desk desk-strange">Strange</span> rounded outline</li>
  </ul>
  <p>This is a new site for a relaunched desk. Older editions from the previous site are not mirrored here.</p>
</main>'''
    return page(
        title="About — What The? News",
        description="What The? News is a WorldTurtleGod Studios project. Editions come from Juno and Vesper. Each story carries its writer's name, sources when needed, and a share link.",
        canonical=f"{SITE_URL}/about/",
        current="about",
        content=content,
    )


def build_authors_index(authors: list[tuple[str, str, int]]) -> str:
    items = []
    for name, slug, count in authors:
        word = "story" if count == 1 else "stories"
        items.append(
            "<li>"
            f'<a href="/authors/{esc(slug)}/">{html.escape(name)}</a>'
            f'<span class="count">{count} {word}</span>'
            "</li>"
        )
    content = f'''<main id="main" class="wrap">
  <header class="page-header">
    <h1 class="page-title">Writers</h1>
    <p class="page-intro">Every story is signed with the writer's name. These are the people behind the bylines.</p>
  </header>
  <ul class="author-index">
    {"".join(items)}
  </ul>
</main>'''
    return page(
        title="Writers — What The? News",
        description="Writers behind What The? News, and the stories with their byline.",
        canonical=f"{SITE_URL}/authors/",
        current="",
        content=content,
    )


def build_archive_page(
    groups: list[tuple[int, date, list[Article]]],
    page_number: int,
    page_count: int,
) -> str:
    blocks = []
    for num, edition_date, articles in groups:
        lead = next((a for a in articles if a.lead), articles[0])
        ordered = [lead] + [a for a in articles if a is not lead]
        heading = f"Edition {num}"
        if page_number == 1 and num == groups[0][0] and page_number:  # latest overall handled by caller sort
            pass
        blocks.append(
            f'<section class="edition-group">'
            f"<h2>{html.escape(heading)} <span class=\"sep\" aria-hidden=\"true\">·</span> {format_date(edition_date)}</h2>"
            f'<div class="story-list">{"".join(story_row_html(a) for a in ordered)}</div>'
            "</section>"
        )
    prev_href = None
    next_href = None
    if page_number > 1:
        prev_href = "/archive/" if page_number == 2 else f"/archive/page/{page_number - 1}/"
    if page_number < page_count:
        next_href = f"/archive/page/{page_number + 1}/"
    suffix = f" — Page {page_number}" if page_number > 1 else ""
    canonical = f"{SITE_URL}/archive/" if page_number == 1 else f"{SITE_URL}/archive/page/{page_number}/"
    content = f'''<main id="main" class="wrap">
  <header class="page-header">
    <h1 class="page-title">Archive</h1>
    <p class="page-intro">Past editions of What The? News, newest first.</p>
  </header>
  {"".join(blocks)}
  {pager_html(prev_href, next_href, "editions")}
</main>'''
    return page(
        title=f"Archive{suffix} — What The? News",
        description="Past editions of What The? News, newest first.",
        canonical=canonical,
        current="archive",
        content=content,
    )


def build_404() -> str:
    content = '''<main id="main" class="wrap">
  <header class="page-header">
    <h1 class="page-title">Page not found</h1>
    <p class="page-intro">That address does not match a story or section on What The? News. Try the <a href="/">home page</a> or the <a href="/archive/">archive</a>.</p>
  </header>
</main>'''
    return page(
        title="Page not found — What The? News",
        description="That address does not match a story or section on What The? News.",
        canonical=f"{SITE_URL}/404.html",
        current="",
        content=content,
    )


def rfc822(value: date) -> str:
    # Publish at 08:00 America/Los_Angeles (UTC-8 in November).
    return value.strftime("%a, %d %b %Y 08:00:00 -0800")


def xml_esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def build_rss(articles: list[Article], latest_num: int, latest_date: date) -> str:
    items = []
    for article in sort_articles(articles)[:25]:
        desc = article.dek or article.title
        items.append(
            "    <item>\n"
            f"      <title>{xml_esc(article.title)}</title>\n"
            f"      <link>{xml_esc(article.url())}</link>\n"
            f"      <guid isPermaLink=\"true\">{xml_esc(article.url())}</guid>\n"
            f"      <pubDate>{rfc822(article.date)}</pubDate>\n"
            f"      <category>{xml_esc(article.desk)}</category>\n"
            f"      <dc:creator>{xml_esc(article.author)}</dc:creator>\n"
            f"      <description>{xml_esc(desc)}</description>\n"
            "    </item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>What The? News</title>\n"
        f"    <link>{SITE_URL}/</link>\n"
        "    <description>A daily paper from WorldTurtleGod Studios. Editions come from Juno and Vesper.</description>\n"
        "    <language>en-us</language>\n"
        f"    <lastBuildDate>{rfc822(latest_date)}</lastBuildDate>\n"
        f'    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        + "\n".join(items)
        + "\n  </channel>\n</rss>\n"
    )


def build_sitemap(urls: list[tuple[str, str]]) -> str:
    # urls: (loc, lastmod ISO date)
    seen = []
    used = set()
    for loc, lastmod in urls:
        if loc not in used:
            used.add(loc)
            seen.append((loc, lastmod))
    body = []
    for loc, lastmod in seen:
        body.append(
            "  <url>\n"
            f"    <loc>{xml_esc(loc)}</loc>\n"
            f"    <lastmod>{xml_esc(lastmod)}</lastmod>\n"
            "  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(body)
        + "\n</urlset>\n"
    )


def all_source_editions() -> list[int]:
    if not SOURCE.is_dir():
        return []
    nums = []
    for folder in SOURCE.iterdir():
        if folder.is_dir() and re.fullmatch(r"\d{3,}", folder.name):
            nums.append(int(folder.name))
    return sorted(nums)


def copy_incoming(num: int, files: list[Path]) -> None:
    dest = SOURCE / edition_pad(num)
    dest.mkdir(parents=True, exist_ok=True)
    for path in files:
        target = dest / path.name
        if path.resolve() != target.resolve():
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"Saved source copy {target.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build What The? News pages from article text files. Nothing is published."
    )
    parser.add_argument(
        "edition",
        nargs="?",
        help="Edition number, like 54 or 054. Skip this if you use --rebuild-all.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Optional article files. If you leave these out, the script reads _source/editions/054/.",
    )
    parser.add_argument(
        "--date",
        dest="date_override",
        help="Edition date as year-month-day, like 2026-11-10.",
    )
    parser.add_argument(
        "--rebuild-all",
        action="store_true",
        help="Rebuild every edition found in _source/editions/, plus the homepage, desks, archive, and feeds.",
    )
    args = parser.parse_args()

    if args.rebuild_all and args.edition:
        fail("Use either an edition number or --rebuild-all, not both.")
    if not args.rebuild_all and not args.edition:
        fail("Please give an edition number, like: python3 tools/new_edition.py 54")

    incoming = [Path(f) for f in args.files]
    for path in incoming:
        if not path.is_file():
            fail(f"Could not find article file: {path}")

    if not args.rebuild_all:
        try:
            num = int(args.edition)
        except ValueError:
            fail(f"Edition should be a number. Got: {args.edition}")
        if num < 1:
            fail("Edition number should be 1 or higher.")
        if incoming:
            copy_incoming(num, incoming)

    nums = all_source_editions()
    if not nums:
        fail("No edition folders found in _source/editions/.")

    # If a specific edition was requested, make sure it exists (or was just copied in).
    if not args.rebuild_all and int(args.edition) not in nums:
        # load will fail with a clear message if the folder is missing
        nums = sorted(set(nums + [int(args.edition)]))

    built: dict[int, tuple[date, list[Article]]] = {}
    date_override_for = int(args.edition) if args.edition and args.date_override else None
    for num in nums:
        override = args.date_override if date_override_for == num else None
        built[num] = load_edition(num, override, None)

    latest = max(built)
    latest_date, latest_articles = built[latest]
    all_articles: list[Article] = []
    for _num in sorted(built):
        all_articles.extend(built[_num][1])
    all_sorted = sort_articles(all_articles)

    clean_generated()

    # Article pages
    by_desk: dict[str, list[Article]] = defaultdict(list)
    by_author: dict[str, list[Article]] = defaultdict(list)
    for article in all_sorted:
        by_desk[article.desk_class].append(article)
        by_author[article.author_slug].append(article)

    for article in all_articles:
        related = by_desk[article.desk_class]
        dest = ROOT / article.path().lstrip("/") / "index.html"
        write(dest, build_article_page(article, related))

    write(ROOT / "index.html", build_index(latest, latest_date, latest_articles, all_articles))
    write(ROOT / "about" / "index.html", build_about())
    write(ROOT / "404.html", build_404())

    # Desk pages
    latest_iso = max(a.date for a in all_articles).isoformat() if all_articles else latest_date.isoformat()
    for desk_class, desk_name in DESK_ORDER:
        stories = by_desk.get(desk_class, [])
        write_paginated_list(
            heading=desk_name,
            intro=f"Stories from the {desk_name} desk, newest first.",
            current=desk_class,
            articles=stories,
            base_dir=ROOT / desk_class,
            base_path=f"/{desk_class}/",
            title=f"{desk_name} — What The? News",
        )

    # Author pages
    author_index: list[tuple[str, str, int]] = []
    seen_authors: dict[str, str] = {}
    for article in all_sorted:
        seen_authors.setdefault(article.author_slug, article.author)
    for slug, name in sorted(seen_authors.items(), key=lambda kv: kv[1].lower()):
        stories = by_author[slug]
        author_index.append((name, slug, len(stories)))
        write_paginated_list(
            heading=name,
            intro=f"Stories by {name}, newest first.",
            current="",
            articles=stories,
            base_dir=ROOT / "authors" / slug,
            base_path=f"/authors/{slug}/",
            title=f"{name} — What The? News",
        )
    write(ROOT / "authors" / "index.html", build_authors_index(author_index))

    # Archive, newest editions first
    edition_list = [
        (num, built[num][0], built[num][1])
        for num in sorted(built.keys(), reverse=True)
    ]
    archive_pages = chunks(edition_list, ARCHIVE_PAGE_SIZE)
    archive_count = max(1, len(archive_pages))
    for i, group in enumerate(archive_pages):
        number = i + 1
        html_page = build_archive_page(group, number, archive_count)
        dest = (
            ROOT / "archive" / "index.html"
            if number == 1
            else ROOT / "archive" / "page" / str(number) / "index.html"
        )
        write(dest, html_page)

    write(ROOT / "feed.xml", build_rss(all_articles, latest, latest_date))

    sitemap_urls: list[tuple[str, str]] = [
        (f"{SITE_URL}/", latest_iso),
        (f"{SITE_URL}/about/", latest_iso),
        (f"{SITE_URL}/archive/", latest_iso),
        (f"{SITE_URL}/authors/", latest_iso),
        (f"{SITE_URL}/feed.xml", latest_iso),
    ]
    for desk_class, _name in DESK_ORDER:
        sitemap_urls.append((f"{SITE_URL}/{desk_class}/", latest_iso))
    for slug, name in seen_authors.items():
        sitemap_urls.append((f"{SITE_URL}/authors/{slug}/", latest_iso))
    for article in all_articles:
        sitemap_urls.append((article.url(), article.date.isoformat()))
    write(ROOT / "sitemap.xml", build_sitemap(sitemap_urls))

    print(f"Homepage is Edition {latest} ({format_date(latest_date)}).")
    print(f"Built {len(all_articles)} articles across {len(built)} editions.")
    if WARNINGS:
        print(f"{len(WARNINGS)} warning(s) printed above.", file=sys.stderr)


if __name__ == "__main__":
    main()
