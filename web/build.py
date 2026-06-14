#!/usr/bin/env python3
"""Generador del códice web de Hierométrica.

Lee el vault de Obsidian (carpeta "Vault Hierométrica") y produce un sitio
estático en web/_site:
  - Resuelve los infobox de Dataview (`=this["Campo"]`) usando el frontmatter.
  - Convierte los bloques `chart` y `dataviewjs` (radar) en canvas de Chart.js.
  - Hace clicables los enlaces [[wiki]].
  - Arma navegación por categorías y un buscador en cliente.

Uso: python3 web/build.py
"""
import json
import re
import shutil
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "Vault Hierométrica"
THEME = ROOT / "web" / "theme"
OUT = ROOT / "web" / "_site"

SITE_TITLE = "Códice de Hierométrica"

# Carpetas que no son contenido del códice
EXCLUDE_DIRS = {"z_Templates", "z_Assets", "copilot", "Excalidraw", ".obsidian"}
# Archivos sueltos a omitir
EXCLUDE_FILES = {"0. Bienvenida.md"}

# Etiquetas legibles para los segmentos de carpeta (se quita el prefijo "N. ")
PREFIX_RE = re.compile(r"^\d+\.\s+")


def deprefix(name: str) -> str:
    return PREFIX_RE.sub("", name)


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text or "nota"


def split_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    if not isinstance(fm, dict):
        fm = {}
    return fm, m.group(2)


# ---------------------------------------------------------------------------
# Carga de notas
# ---------------------------------------------------------------------------
class Note:
    def __init__(self, path: Path):
        self.path = path
        rel = path.relative_to(VAULT)
        self.rel_parts = list(rel.parts)
        self.name = path.stem
        self.raw = path.read_text(encoding="utf-8")
        self.frontmatter, self.body = split_frontmatter(self.raw)
        self.slug = slugify("-".join(deprefix(p) for p in rel.with_suffix("").parts))
        self.url = self.slug + ".html"
        # categoría = primer subnivel significativo
        parts = [deprefix(p) for p in self.rel_parts[:-1]]
        # parts[0] suele ser "Enciclopedia" o "Prosa"
        self.section = parts[1] if len(parts) > 1 else (parts[0] if parts else "General")
        self.subsection = parts[2] if len(parts) > 2 else None
        self.top = parts[0] if parts else "General"
        self.infobox = None
        self.body_html = ""
        self.charts = []
        self.plain_text = ""


def collect_notes():
    notes = []
    for p in sorted(VAULT.rglob("*.md")):
        rel = p.relative_to(VAULT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if p.name in EXCLUDE_FILES:
            continue
        notes.append(Note(p))
    return notes


# ---------------------------------------------------------------------------
# Resolución de expresiones de Dataview e infobox
# ---------------------------------------------------------------------------
def fm_clean(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value).strip()


def resolve_this(expr: str, note: Note) -> str:
    expr = expr.strip()
    if expr == "this.file.name":
        return note.name
    m = re.match(r'this\["?([^"\]]+)"?\]', expr) or re.match(r"this\.([\w-]+)", expr)
    if m:
        return fm_clean(note.frontmatter.get(m.group(1), ""))
    return ""


def resolve_inline_queries(text: str, note: Note) -> str:
    return re.sub(r"`=([^`]+)`", lambda m: resolve_this(m.group(1), note), text)


# ---------------------------------------------------------------------------
# Wikilinks e imágenes embebidas
# ---------------------------------------------------------------------------
def render_wikilinks(text: str, name_index: dict) -> str:
    def repl(m):
        target = m.group(1).strip()
        alias = m.group(3)
        label = (alias or target).strip()
        slug = name_index.get(target.lower())
        if slug:
            return f'<a class="wikilink" href="{slug}.html">{label}</a>'
        return f'<span class="wikilink missing" title="Aún no existe esta nota">{label}</span>'

    return re.sub(r"\[\[([^\]|]+?)(\|([^\]]+))?\]\]", repl, text)


def asset_for_embed(target: str):
    """Devuelve el nombre de archivo de asset para un embed de imagen."""
    base = target.split("|")[0].split("/")[-1].strip()
    if re.search(r"\.(webp|png|jpe?g|gif|svg)$", base, re.IGNORECASE):
        return base
    return None


# ---------------------------------------------------------------------------
# Infobox
# ---------------------------------------------------------------------------
def parse_infobox(body: str, note: Note, name_index: dict):
    lines = body.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("> [!infobox]"):
            start = i
            break
    if start is None:
        return None, body

    block = []
    end = start
    for i in range(start + 1, len(lines)):
        if lines[i].startswith(">"):
            block.append(lines[i][1:].lstrip())
            end = i
        elif lines[i].strip() == "":
            # permitir líneas en blanco dentro del callout solo si siguen más '>'
            if i + 1 < len(lines) and lines[i + 1].startswith(">"):
                continue
            break
        else:
            break

    remaining = "\n".join(lines[:start] + lines[end + 1:])

    ib = {"title": note.name, "subtitle": "", "image": None, "sections": []}
    current = None
    for ln in block:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("# "):
            inner = resolve_inline_queries(s[2:], note)
            inner = re.sub(r"<font[^>]*>", "", inner)
            inner = inner.replace("</font>", "")
            inner = inner.replace("*", "").strip()
            if ib.get("_has_title"):
                ib["subtitle"] = inner
            else:
                ib["title"] = inner or note.name
                ib["_has_title"] = True
        elif s.startswith("![["):
            m = re.search(r"!\[\[([^\]]+)\]\]", s)
            if m:
                ib["image"] = asset_for_embed(m.group(1))
        elif s.startswith("######"):
            head = s.lstrip("#").strip()
            head_html = render_wikilinks(head, name_index)
            current = {"name": head_html, "rows": []}
            ib["sections"].append(current)
        elif "|" in s:
            if re.match(r"^[\s|:-]+$", s):
                continue
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if not cells or cells[0].lower() == "campo":
                continue
            key = cells[0]
            val = cells[1] if len(cells) > 1 else ""
            val = resolve_inline_queries(val, note)
            val = render_wikilinks(val, name_index)
            if val.strip():  # ocultar filas vacías
                if current is None:
                    current = {"name": "", "rows": []}
                    ib["sections"].append(current)
                current["rows"].append({"k": key, "v": val})
    # quitar secciones sin filas
    ib["sections"] = [s for s in ib["sections"] if s["rows"]]
    ib.pop("_has_title", None)
    return ib, remaining


# ---------------------------------------------------------------------------
# Gráficos (chart / dataviewjs radar)
# ---------------------------------------------------------------------------
def extract_charts(body: str, note: Note):
    charts = []

    def chart_repl(m):
        try:
            cfg = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            return ""
        labels = cfg.get("labels") or []
        series = cfg.get("series") or []
        datasets = []
        for s in series:
            datasets.append({"label": s.get("title", ""), "data": s.get("data", [])})
        if not labels or not datasets:
            return ""
        idx = len(charts)
        charts.append({"type": cfg.get("type", "radar"), "labels": labels,
                       "datasets": datasets, "fill": bool(cfg.get("fill", True))})
        return f'\n<<<CHART:{idx}>>>\n'

    body = re.sub(r"```chart\s*\n(.*?)```", chart_repl, body, flags=re.DOTALL)

    def dvjs_repl(m):
        block = m.group(1)
        labels = re.search(r"labels:\s*(\[[^\]]*\])", block)
        data = re.search(r"data:\s*(\[[^\]]*\])", block)
        if not (labels and data):
            return ""
        try:
            lbls = json.loads(labels.group(1))
            dta = json.loads(data.group(1))
        except json.JSONDecodeError:
            return ""
        idx = len(charts)
        charts.append({"type": "radar", "labels": lbls,
                       "datasets": [{"label": "Stats", "data": dta}], "fill": True})
        return f'\n<<<CHART:{idx}>>>\n'

    body = re.sub(r"```dataviewjs\s*\n(.*?)```", dvjs_repl, body, flags=re.DOTALL)
    return body, charts


# ---------------------------------------------------------------------------
# Cuerpo markdown -> HTML (parser ligero)
# ---------------------------------------------------------------------------
def render_inline_md(text: str, name_index: dict) -> str:
    text = render_wikilinks(text, name_index)
    text = re.sub(r"!\[\[([^\]]+)\]\]", "", text)  # embeds restantes
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text


def render_body(body: str, note: Note, name_index: dict, charts) -> str:
    out = []
    in_list = False
    paragraph = []

    def flush_p():
        nonlocal paragraph
        if paragraph:
            joined = " ".join(paragraph).strip()
            if joined:
                out.append(f"<p>{render_inline_md(joined, name_index)}</p>")
            paragraph = []

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in body.splitlines():
        line = raw.rstrip()
        cm = re.match(r"<<<CHART:(\d+)>>>", line.strip())
        if cm:
            flush_p(); close_list()
            i = int(cm.group(1))
            out.append(f'<div class="chartwrap"><canvas data-chart=\'{json.dumps(charts[i])}\'></canvas></div>')
            continue
        if not line.strip():
            flush_p(); close_list()
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", line)
        if h:
            flush_p(); close_list()
            level = len(h.group(1))
            heading_text = h.group(2).strip()
            # el H1 del cuerpo suele repetir el título de la nota: se omite
            if level == 1 and heading_text in (note.name, "`=this.file.name`"):
                continue
            content = render_inline_md(heading_text, name_index)
            if content.strip():
                out.append(f"<h{level}>{content}</h{level}>")
            continue
        if line.lstrip().startswith(("- ", "* ")):
            flush_p()
            if not in_list:
                out.append("<ul>"); in_list = True
            item = line.lstrip()[2:]
            out.append(f"<li>{render_inline_md(item, name_index)}</li>")
            continue
        if line.lstrip().startswith("> "):
            flush_p(); close_list()
            out.append(f"<blockquote>{render_inline_md(line.lstrip()[2:], name_index)}</blockquote>")
            continue
        if line.startswith("#") and not h:  # tags como #inline-events
            continue
        paragraph.append(line.strip())

    flush_p(); close_list()
    return "\n".join(out)


def plain_text_of(note: Note) -> str:
    txt = re.sub(r"```.*?```", " ", note.body, flags=re.DOTALL)
    txt = re.sub(r"[>#*`\[\]|]", " ", txt)
    txt = re.sub(r"=this\S*", " ", txt)
    txt = re.sub(r"\s+", " ", txt)
    return txt.strip()[:500]


# ---------------------------------------------------------------------------
# Plantillas HTML
# ---------------------------------------------------------------------------
def page_shell(title, body_inner, nav_html, depth_note=True):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {SITE_TITLE}</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<button id="menu-toggle" aria-label="Menú">☰</button>
<aside id="sidebar">
  <a class="brand" href="index.html">{SITE_TITLE}</a>
  <div class="search-box"><input id="search" type="search" placeholder="Buscar en el códice…" autocomplete="off"><div id="search-results"></div></div>
  <nav>{nav_html}</nav>
</aside>
<main>{body_inner}</main>
<script src="assets/chart.umd.js"></script>
<script src="assets/search-index.js"></script>
<script src="assets/app.js"></script>
</body>
</html>"""


def render_infobox_html(ib):
    if not ib:
        return ""
    parts = ['<div class="infobox">']
    parts.append(f'<div class="ib-title">{ib["title"]}</div>')
    if ib.get("subtitle"):
        parts.append(f'<div class="ib-subtitle">{ib["subtitle"]}</div>')
    if ib.get("image"):
        parts.append(f'<div class="ib-image"><img src="assets/vault/{ib["image"]}" alt=""></div>')
    for sec in ib["sections"]:
        if sec["name"]:
            parts.append(f'<div class="ib-section">{sec["name"]}</div>')
        parts.append('<table class="ib-table">')
        for row in sec["rows"]:
            parts.append(f'<tr><th>{row["k"]}</th><td>{row["v"]}</td></tr>')
        parts.append("</table>")
    parts.append("</div>")
    return "\n".join(parts)


def render_note_page(note: Note, nav_html):
    crumb = " › ".join([note.top] + ([note.section] if note.section != note.top else [])
                       + ([note.subsection] if note.subsection else []))
    body_html = note.body_html or '<p class="empty">Esta página todavía no tiene contenido.</p>'
    inner = ['<article class="note">']
    inner.append(f'<div class="breadcrumb">{crumb}</div>')
    inner.append(f'<h1 class="note-title">{note.name}</h1>')
    inner.append('<div class="note-layout">')
    inner.append(f'<div class="note-body">{body_html}</div>')
    inner.append(render_infobox_html(note.infobox))
    inner.append("</div></article>")
    return page_shell(note.name, "\n".join(inner), nav_html)


def build_nav(notes):
    """Agrupa por top -> section -> (subsection) -> notas."""
    tree = {}
    for n in notes:
        tree.setdefault(n.top, {}).setdefault(n.section, {}).setdefault(n.subsection or "", []).append(n)

    html = []
    for top in sorted(tree):
        html.append(f'<div class="nav-top">{top}</div>')
        for section in sorted(tree[top]):
            subs = tree[top][section]
            html.append('<details class="nav-section" open>')
            html.append(f"<summary>{section}</summary>")
            for sub in sorted(subs):
                if sub:
                    html.append(f'<div class="nav-sub">{sub}</div>')
                html.append("<ul>")
                for n in sorted(subs[sub], key=lambda x: x.name):
                    html.append(f'<li><a href="{n.url}">{n.name}</a></li>')
                html.append("</ul>")
            html.append("</details>")
    return "\n".join(html)


def render_home(notes, nav_html):
    cards = []
    by_section = {}
    for n in notes:
        by_section.setdefault(n.section, []).append(n)
    for section in sorted(by_section):
        items = sorted(by_section[section], key=lambda x: x.name)
        links = "".join(f'<li><a href="{n.url}">{n.name}</a></li>' for n in items[:8])
        cards.append(f'<div class="home-card"><h3>{section}</h3><ul>{links}</ul></div>')
    inner = f"""
<div class="home-banner"><img src="assets/banner.webp" alt=""><div class="home-banner-text"><h1>{SITE_TITLE}</h1><p>Enciclopedia del mundo y su sistema de magia, la Hierométrica.</p></div></div>
<section class="home-grid">{''.join(cards)}</section>
"""
    return page_shell("Inicio", inner, nav_html)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    assets = OUT / "assets"
    assets.mkdir()
    (assets / "vault").mkdir()

    notes = collect_notes()
    name_index = {n.name.lower(): n.slug for n in notes}

    for n in notes:
        ib, body_wo_ib = parse_infobox(n.body, n, name_index)
        n.infobox = ib
        body_wo_ib = resolve_inline_queries(body_wo_ib, n)
        body_wo_charts, charts = extract_charts(body_wo_ib, n)
        n.charts = charts
        n.body_html = render_body(body_wo_charts, n, name_index, charts)
        n.plain_text = plain_text_of(n)

    nav_html = build_nav(notes)

    for n in notes:
        (OUT / n.url).write_text(render_note_page(n, nav_html), encoding="utf-8")

    (OUT / "index.html").write_text(render_home(notes, nav_html), encoding="utf-8")

    # assets de tema
    shutil.copy(THEME / "chart.umd.js", assets / "chart.umd.js")
    shutil.copy(THEME / "style.css", assets / "style.css")
    shutil.copy(THEME / "app.js", assets / "app.js")
    if (THEME / "banner.webp").exists():
        shutil.copy(THEME / "banner.webp", assets / "banner.webp")

    # imágenes del vault
    vault_assets = VAULT / "z_Assets"
    if vault_assets.exists():
        for img in vault_assets.rglob("*"):
            if img.suffix.lower() in {".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg"}:
                shutil.copy(img, assets / "vault" / img.name)

    # índice de búsqueda
    index = [{"t": n.name, "u": n.url, "s": n.section, "x": n.plain_text} for n in notes]
    (assets / "search-index.js").write_text(
        "window.SEARCH_INDEX = " + json.dumps(index, ensure_ascii=False) + ";",
        encoding="utf-8")

    print(f"Generadas {len(notes)} notas + portada en {OUT}")


if __name__ == "__main__":
    main()
