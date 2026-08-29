#!/usr/bin/env python3
"""Convert QGA book Markdown chapters to LaTeX chapter files.

Usage (from repo root):
  python3 scripts/md_to_latex.py
  python3 scripts/md_to_latex.py --only 01_quaternions.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"
OUT = ROOT / "book" / "latex" / "chapters"

# Map markdown filenames → (latex_basename, kind)
# kind: chapter | chapter* | front
CHAPTERS = [
    ("00_preface.md", "preface", "front"),
    ("HOW_TO_USE.md", "how_to_use", "front"),
    ("00_preview.md", "ch00_preview", "chapter"),
    ("01_quaternions.md", "ch01_quaternions", "chapter"),
    ("02_hopf.md", "ch02_hopf", "chapter"),
    ("03_gauged_hopf_lattice.md", "ch03_lattice", "chapter"),
    ("04_symmetries.md", "ch04_symmetries", "chapter"),
    ("05_forms_topographs.md", "ch05_topographs", "chapter"),
    ("06_classification.md", "ch06_classification", "chapter"),
    ("07_representations_z_flux.md", "ch07_z_map", "chapter"),
    ("08_class_group.md", "ch08_class_group", "chapter"),
    ("09_quaternion_algebras.md", "ch09_algebras", "chapter"),
    ("10_observations_emergent.md", "ch10_observations", "chapter"),
    # Appendices (unnumbered chapters in back matter)
    ("A_terminology_notation.md", "app_a_terminology", "appendix"),
    ("B_open_problems.md", "app_b_open_problems", "appendix"),
    ("C_lab_code_reference.md", "app_c_labs", "appendix"),
    ("D_validation_t4.md", "app_d_validation", "appendix"),
    ("E_figure_atlas.md", "app_e_figures", "appendix"),
    ("F_hatcher_dictionary.md", "app_f_hatcher", "appendix"),
]


# Punctuation → ASCII (safe to run before LaTeX escaping).
_UNICODE_PUNCT = {
    "\u2014": "---",
    "\u2013": "--",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2026": "...",
    "\u00a0": " ",
    "\u2212": "-",
    "\u2500": "-",
    "\u2514": "+",
    "\u251c": "+",
    "\ufffd": "",
}

# Math/symbol unicode → LaTeX commands. Applied *after* escaping so
# backslashes are not turned into \textbackslash{}.
# Never map unknown code points to "?": that produced 350/? / stripped bars.
_UNICODE_MATH = {
    "\u2192": r"\(\rightarrow\)",
    "\u21a6": r"\(\mapsto\)",
    "\u2190": r"\(\leftarrow\)",
    "\u2194": r"\(\leftrightarrow\)",
    "\u00d7": r"\(\times\)",
    "\u2248": r"\(\approx\)",
    "\u2260": r"\(\neq\)",
    "\u2264": r"\(\leq\)",
    "\u2265": r"\(\geq\)",
    "\u00b7": r"\(\cdot\)",
    "\u221e": r"\(\infty\)",
    "\u21d2": r"\(\Rightarrow\)",
    "\u2261": r"\(\equiv\)",
    "\u03c0": r"\(\pi\)",
    "\u03ba": r"\(\kappa\)",
    "\u03b1": r"\(\alpha\)",
    "\u03be": r"\(\xi\)",
    "\u03b7": r"\(\eta\)",
    "\u03c6": r"\(\phi\)",
    "\u03c8": r"\(\psi\)",
    "\u2081": r"\(_1\)",
    "\u2082": r"\(_2\)",
    "\u2083": r"\(_3\)",
    "\u00a7": r"\S{}",
    "\u2229": r"\(\cap\)",
    "\u203e": r"\(\overline{\,\cdot\,}\)",
    "\u25ba": r"\(\triangleright\)",
    "\u25c4": r"\(\triangleleft\)",
}

_LISTING_ASCII = {
    "\u2014": "--",
    "\u2013": "-",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2026": "...",
    "\u00a0": " ",
    "\u2192": "->",
    "\u21a6": "|->",
    "\u2190": "<-",
    "\u2194": "<->",
    "\u03c0": "pi",
    "\u03ba": "kappa",
    "\u03b1": "alpha",
    "\u03be": "xi",
    "\u03b7": "eta",
    "\u03c6": "phi",
    "\u03c8": "psi",
    "\u2081": "1",
    "\u2082": "2",
    "\u2083": "3",
    "\u00a7": "S",
    "\u00b7": ".",
    "\u203e": "bar",
    "\u221e": "inf",
    "\u2264": "<=",
    "\u2265": ">=",
    "\u2260": "!=",
    "\u00d7": "x",
    "\u2229": "cap",
    "\u2500": "-",
    "\u2514": "+",
    "\u251c": "+",
    "\u25ba": ">",
    "\u25c4": "<",
}


def normalize_punctuation(s: str) -> str:
    """ASCII punctuation only. Unknown non-ASCII is left intact (never '?')."""
    for a, b in _UNICODE_PUNCT.items():
        s = s.replace(a, b)
    return s


def inject_unicode_math(s: str) -> str:
    """Insert LaTeX math commands for remaining symbol unicode."""
    for a, b in _UNICODE_MATH.items():
        s = s.replace(a, b)
    return s


def normalize_unicode(s: str) -> str:
    """Map common Unicode punctuation and math to LaTeX-friendly forms.

    Curly double quotes must NOT become backticks: that confuses inline-code
    extraction and can swallow whole sentences (including math) into \\texttt.
    """
    return inject_unicode_math(normalize_punctuation(s))


def listing_ascii(s: str) -> str:
    """ASCII-safe listings body: named replacements, no '?' black-hole."""
    for a, b in _LISTING_ASCII.items():
        s = s.replace(a, b)
    out = []
    for ch in s:
        o = ord(ch)
        if o < 128:
            out.append(ch)
        else:
            out.append(f"[U+{o:04X}]")
    return "".join(out)


_BAKED_HEADING_NUM = re.compile(
    r"^(?:(?:Chapter|Appendix|Section)\s+)?"
    r"(?:[A-Z]\.)?\d+(?:\.\d+)*"
    r"(?:\s*[\u2014\u2013:—.–-]+\s*|\s+)",
    re.IGNORECASE,
)


def strip_baked_heading_number(title: str) -> str:
    """Drop '2.1 ' / 'C.1 ' / 'Chapter 2 — ' so LaTeX counters number headings."""
    t = title.strip()
    t = re.sub(
        r"^Chapter\s+\d+\s*[\u2014\u2013—–-]+\s*",
        "",
        t,
        flags=re.I,
    )
    t = re.sub(
        r"^Appendix\s+[A-Z]\s*[\u2014\u2013—–-]+\s*",
        "",
        t,
        flags=re.I,
    )
    m = _BAKED_HEADING_NUM.match(t)
    if m:
        t = t[m.end() :]
    return t.strip() or title.strip()


def escape_text(s: str) -> str:
    """Escape LaTeX specials outside math. Punctuation only — no math inject."""
    s = normalize_punctuation(s)
    out = s.replace("\\", "\x00BS\x00")
    for a, b in [
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        out = out.replace(a, b)
    out = out.replace("\x00BS\x00", r"\textbackslash{}")
    return out


def latex_quotes(s: str) -> str:
    """Turn ASCII double quotes into LaTeX `` '' pairs (best-effort)."""
    parts = s.split('"')
    if len(parts) == 1:
        return s
    out: list[str] = []
    for i, part in enumerate(parts):
        out.append(part)
        if i < len(parts) - 1:
            out.append("``" if i % 2 == 0 else "''")
    return "".join(out)


def latex_code_span(content: str) -> str:
    """Inline code as breakable \\texttt (safe in headings and tables).

    Avoid \\path here: it is fragile in moving arguments (section titles /
    PDF bookmarks). Insert discretionary breaks after / . _ : so long paths
    wrap inside tabularx X columns.
    """
    escaped = escape_text(listing_ascii(content))
    for ch, repl in (
        ("/", r"/\allowbreak{}"),
        (".", r".\allowbreak{}"),
        (":", r":\allowbreak{}"),
        (r"\_", r"\_\allowbreak{}"),
        (r"\textasciitilde{}", r"\textasciitilde{}\allowbreak{}"),
    ):
        escaped = escaped.replace(ch, repl)
    return r"\texttt{" + escaped + "}"


_MARK_RE = re.compile(
    r"(\x00PH\d+\x00|\x00BSTART\x00|\x00BEND\x00|\x00ISTART\x00|\x00IEND\x00)"
)
_FIG_ITALIC = re.compile(
    r"^\*(?:Auxiliary\s+)?Figure\s+[A-Z]?\d+(?:\.\d+)*"
    r"(?:\s*[\u2014\u2013—–:-]+\s*|\s+)?"
    r"(.*?)\.\*\s*(.*)$",
    re.I,
)
_FIG_PREFIX = re.compile(
    r"^(?:Auxiliary\s+)?Figure\s+[A-Z]?\d+(?:\.\d+)*\s*(?:[\u2014\u2013—–:.\-]+)\s*",
    re.I,
)


def figure_caption_text(alt: str, italic_line: str | None) -> str:
    """Body of a figure caption without a leading 'Figure x.y' label.

    LaTeX ``\\caption`` already prints ``Figure N:``; keeping the manuscript
    tag in the body produced stacked labels (``Figure 4: Figure 0.4``).
    """
    if italic_line:
        m = _FIG_ITALIC.match(italic_line.strip())
        if m:
            title = (m.group(1) or "").strip()
            rest = (m.group(2) or "").strip()
            if title and rest:
                if title.endswith("."):
                    return f"{title} {rest}"
                return f"{title}. {rest}"
            return rest or title
        body = italic_line.strip().strip("*").strip()
        stripped = _FIG_PREFIX.sub("", body).strip()
        return stripped or body
    stripped = _FIG_PREFIX.sub("", alt.strip()).strip()
    return stripped or alt.strip()


def convert_inline(s: str) -> str:
    r"""Convert inline markdown; leave \( \) and existing math alone.

    Math/code/links are stashed as placeholders so **bold** may wrap math
    without leftover markdown (e.g. **angle-chart \(\xi_2\)-circle**).
    Unicode mapping is applied to *text* only so math is not nested as
    \(\(\pi\)\) and overlines in \(N(q)=q\overline{q}\) survive.
    """
    stored: list[tuple[str, str]] = []

    def stash(kind: str, content: str) -> str:
        stored.append((kind, content))
        return f"\x00PH{len(stored) - 1}\x00"

    # Extract math / code / bare URLs first. Math before code.
    # Do not map curly quotes to backticks (breaks code-span detection).
    # Order matters: math → full markdown links → code → bare URLs.
    # Links before code so [`path`](url) is not split on the inner backticks.
    pattern = re.compile(
        r"("
        r"\\\(.+?\\\)"
        r"|\\\[.+?\\\]"
        r"|\$\$.+?\$\$"
        r"|\$(?!\$)(?:\\.|[^$\\])+\$"
        r"|\[[^\]]+\]\([^)]+\)"
        r"|`[^`\n]+`"
        r"|(?<!\]\()https?://[^\s|<>()]+"
        r")"
    )
    pieces: list[str] = []
    pos = 0
    for m in pattern.finditer(s):
        if m.start() > pos:
            pieces.append(s[pos : m.start()])
        tok = m.group(0)
        if tok.startswith("[") and "](" in tok:
            pieces.append(stash("link", tok))
        elif tok.startswith("`"):
            pieces.append(stash("code", tok[1:-1]))
        elif tok.startswith("$$"):
            pieces.append(stash("dmath", tok[2:-2]))
        elif tok.startswith("\\["):
            pieces.append(stash("dmath", tok[2:-2]))
        elif tok.startswith("\\("):
            pieces.append(stash("imath", tok[2:-2]))
        elif tok.startswith("$"):
            pieces.append(stash("imath", tok[1:-1]))
        elif tok.startswith("http"):
            pieces.append(stash("url", tok.rstrip(".,;:)")))
        else:
            pieces.append(tok)
        pos = m.end()
    if pos < len(s):
        pieces.append(s[pos:])
    text = "".join(pieces)

    text = latex_quotes(normalize_punctuation(text))
    text = re.sub(
        r"\*\*(.+?)\*\*",
        lambda m: "\x00BSTART\x00" + m.group(1) + "\x00BEND\x00",
        text,
    )
    text = re.sub(
        r"(?<!\*)\*([^*]+?)\*(?!\*)",
        lambda m: "\x00ISTART\x00" + m.group(1) + "\x00IEND\x00",
        text,
    )

    def render_stashed(kind: str, content: str) -> str:
        if kind == "link":
            lm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", content)
            if not lm:
                return inject_unicode_math(escape_text(content))
            label_raw, url = lm.group(1), lm.group(2)
            if "`" in label_raw or "*" in label_raw or "\\" in label_raw:
                label_tex = convert_inline(label_raw)
            else:
                label_tex = escape_text(label_raw)
            url_tex = url.replace("%", r"\%").replace("#", r"\#")
            return rf"\href{{{url_tex}}}{{{label_tex}}}"
        if kind == "code":
            return latex_code_span(content)
        if kind == "url":
            safe = content.replace("%", r"\%").replace("#", r"\#")
            return r"\url{" + safe + "}"
        if kind == "imath":
            return r"\(" + content + r"\)"
        if kind == "dmath":
            return "\n\\[\n" + content.strip() + "\n\\]\n"
        return inject_unicode_math(escape_text(content))

    out: list[str] = []
    for tok in _MARK_RE.split(text):
        if not tok:
            continue
        pm = re.fullmatch(r"\x00PH(\d+)\x00", tok)
        if pm:
            kind, content = stored[int(pm.group(1))]
            out.append(render_stashed(kind, content))
        elif tok == "\x00BSTART\x00":
            out.append(r"\textbf{")
        elif tok == "\x00BEND\x00":
            out.append("}")
        elif tok == "\x00ISTART\x00":
            out.append(r"\emph{")
        elif tok == "\x00IEND\x00":
            out.append("}")
        else:
            out.append(inject_unicode_math(escape_text(tok)))
    return "".join(out)


def slugify(title: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-").lower()
    return s[:60] or "sec"


def convert_table(rows: list[str]) -> str:
    """Convert markdown table lines to full-width booktabs tabularx.

    Prefer margin-to-margin width (\\textwidth) with ragged X columns so
    long paths / roles wrap instead of overlapping. First column is a modest
    fixed width for short tags (Fig. 0.1, Label, …); remaining columns share
    the rest of the line.
    """
    parsed = []
    for row in rows:
        row = row.strip().strip("|")
        cells = [c.strip() for c in row.split("|")]
        parsed.append(cells)
    if len(parsed) < 2:
        return "\n".join(convert_inline(r) for r in rows)

    # drop separator row
    body = [parsed[0]]
    for r in parsed[1:]:
        if all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in r):
            continue
        body.append(r)

    ncols = max(len(r) for r in body)
    for r in body:
        while len(r) < ncols:
            r.append("")

    # Full-width tabularx; ragged wrapping in every flexible column.
    X = r">{\raggedright\arraybackslash}X"
    # Narrow tag column for Fig./Aux./OP labels (3-col figure tables)
    L = r">{\raggedright\arraybackslash}p{0.12\textwidth}"
    header_l = " ".join(body[0]).lower()
    if ncols == 1:
        colspec = X
    elif ncols == 2 and "claim" in header_l:
        # Claim-discipline tables: wide claim, short type — do not truncate.
        colspec = (
            r">{\raggedright\arraybackslash}p{0.70\textwidth}"
            r">{\raggedright\arraybackslash}X"
        )
    elif ncols == 2:
        # Path|Role, Resource|Location — both columns need wrap room
        colspec = X + X
    elif ncols == 3:
        # Tag | File | Role (common chapter figure tables)
        colspec = L + X + X
    else:
        # 4+ columns: equal flexible share, margin-to-margin
        colspec = X * ncols

    lines = [
        r"\begin{center}",
        r"\small",
        r"\setlength{\tabcolsep}{4pt}",
        rf"\begin{{tabularx}}{{\textwidth}}{{@{{}}{colspec}@{{}}}}",
        r"\toprule",
    ]
    # header
    hdr = " & ".join(convert_inline(c) for c in body[0]) + r" \\"
    lines.append(hdr)
    lines.append(r"\midrule")
    for r in body[1:]:
        lines.append(" & ".join(convert_inline(c) for c in r) + r" \\")
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabularx}",
            r"\end{center}",
            "",
        ]
    )
    return "\n".join(lines)


def convert_file(md_path: Path, kind: str, label_base: str) -> str:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    out.append(f"% Auto-generated from book/{md_path.name} — do not edit by hand")
    out.append(f"% Regenerated by scripts/md_to_latex.py")
    out.append("")

    i = 0
    in_code = False
    code_lang = ""
    code_buf: list[str] = []
    first_heading = True
    para_buf: list[str] = []

    def flush_para():
        nonlocal para_buf
        if not para_buf:
            return
        text = " ".join(para_buf)
        # orphan italic captions (normally consumed with the image)
        m = _FIG_ITALIC.match(text)
        if m:
            body = figure_caption_text("", text)
            out.append(r"\begin{quote}\small\textit{" + convert_inline(body) + r"}\end{quote}")
            out.append("")
            para_buf = []
            return
        out.append(convert_inline(text))
        out.append("")
        para_buf = []

    while i < len(lines):
        line = lines[i]

        # code fence
        if line.startswith("```"):
            flush_para()
            if not in_code:
                in_code = True
                code_lang = line[3:].strip()
                code_buf = []
            else:
                in_code = False
                content = "\n".join(code_buf)
                # escape for listings
                content = content.replace("\\", "\\textbackslash{}")  # listings uses escape?
                # use verbatim-ish listings with escape disabled
                lang = code_lang if code_lang in ("python", "bash", "text", "") else "text"
                if lang == "":
                    lang = "text"
                out.append(r"\begin{lstlisting}[style=qga" + (f",language={lang}" if lang == "python" else "") + "]")
                # listings: write raw but escape only { } for safety in basic
                # listings + pdflatex: keep ASCII only
                raw = listing_ascii("\n".join(code_buf))
                out.append(raw)
                out.append(r"\end{lstlisting}")
                out.append("")
                code_buf = []
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # manuscript footer italics — drop, do not convert (nested \texttt breaks strip)
        if re.match(r"^\*Manuscript\b", line.strip()):
            flush_para()
            i += 1
            continue

        # blank
        if not line.strip():
            flush_para()
            i += 1
            continue

        # horizontal rule
        if re.match(r"^-{3,}\s*$", line) or re.match(r"^\*{3,}\s*$", line):
            flush_para()
            out.append(r"\bigskip")
            out.append(r"\noindent\rule{\textwidth}{0.4pt}")
            out.append(r"\bigskip")
            out.append("")
            i += 1
            continue

        # image
        mimg = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line.strip())
        if mimg:
            flush_para()
            alt, path = mimg.group(1), mimg.group(2)
            # path figures/foo.png → figures/foo (basename)
            path = path.replace("figures/", "")
            # caption from following italic line (blank line allowed)
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            italic = None
            if j < len(lines) and re.match(
                r"^\*(?:Auxiliary\s+)?Figure\b", lines[j].strip(), re.I
            ):
                italic = lines[j].strip()
                i = j
            caption = figure_caption_text(alt, italic)
            label = "fig:" + slugify(Path(path).stem)
            out.append(r"\begin{figure}[htbp]")
            out.append(r"  \centering")
            out.append(
                rf"  \includegraphics[width=0.92\textwidth,height=0.42\textheight,keepaspectratio]{{{path}}}"
            )
            out.append(rf"  \caption{{{convert_inline(caption)}}}")
            out.append(rf"  \label{{{label}}}")
            out.append(r"\end{figure}")
            out.append("")
            i += 1
            continue

        # table block
        if "|" in line and line.strip().startswith("|"):
            flush_para()
            trows = []
            while i < len(lines) and "|" in lines[i]:
                trows.append(lines[i])
                i += 1
            out.append(convert_table(trows))
            out.append("")
            continue

        # headings
        hm = re.match(r"^(#{1,4})\s+(.*)$", line)
        if hm:
            flush_para()
            level = len(hm.group(1))
            title = hm.group(2).strip()
            numbered_title = strip_baked_heading_number(title)
            # strip trailing markdown emphasis
            title_tex = convert_inline(numbered_title)
            if level == 1:
                if first_heading:
                    first_heading = False
                    plain = escape_text(re.sub(r"\*\*|__|`", "", numbered_title))
                    if kind == "front":
                        out.append(rf"\chapter*{{{title_tex}}}")
                        out.append(rf"\label{{{label_base}}}")
                        out.append(rf"\addcontentsline{{toc}}{{chapter}}{{{plain}}}")
                        out.append(rf"\markboth{{{plain}}}{{}}")
                    elif kind == "appendix":
                        short_tex = convert_inline(numbered_title)
                        out.append(rf"\chapter{{{short_tex}}}")
                        out.append(rf"\label{{{label_base}}}")
                    else:
                        out.append(rf"\chapter{{{title_tex}}}")
                        out.append(rf"\label{{{label_base}}}")
                else:
                    out.append(rf"\section*{{{title_tex}}}")
            elif level == 2:
                lab = f"{label_base}:{slugify(numbered_title)}"
                cmd = r"\section*" if kind == "front" else r"\section"
                out.append(rf"{cmd}{{{title_tex}}}")
                out.append(rf"\label{{{lab}}}")
            elif level == 3:
                lab = f"{label_base}:{slugify(numbered_title)}"
                cmd = r"\subsection*" if kind == "front" else r"\subsection"
                out.append(rf"{cmd}{{{title_tex}}}")
                out.append(rf"\label{{{lab}}}")
            else:
                cmd = r"\subsubsection*" if kind == "front" else r"\subsubsection"
                out.append(rf"{cmd}{{{title_tex}}}")
            out.append("")
            i += 1
            continue

        # numbered list item
        if re.match(r"^\d+\.\s+", line):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]))
                i += 1
            out.append(r"\begin{enumerate}")
            for it in items:
                out.append(r"\item " + convert_inline(it))
            out.append(r"\end{enumerate}")
            out.append("")
            continue

        # bullet list
        if re.match(r"^[-*]\s+", line):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append(re.sub(r"^[-*]\s+", "", lines[i]))
                i += 1
            out.append(r"\begin{itemize}")
            for it in items:
                out.append(r"\item " + convert_inline(it))
            out.append(r"\end{itemize}")
            out.append("")
            continue

        # block math alone
        if line.strip() in (r"\[", "$$") or line.strip().startswith(r"\["):
            flush_para()
            if line.strip() in ("$$", r"\["):
                buf = []
                i += 1
                while i < len(lines) and lines[i].strip() not in ("$$", r"\]"):
                    buf.append(lines[i])
                    i += 1
                if i < len(lines):
                    i += 1
                out.append("\\[")
                out.append("\n".join(buf))
                out.append("\\]")
                out.append("")
            else:
                # whole line \[ ... \]
                out.append(line)
                out.append("")
                i += 1
            continue

        # LaTeX environments pass through raw (align*, equation*, etc.)
        if line.strip().startswith("\\begin{"):
            flush_para()
            env = line.strip()
            out.append(env)
            i += 1
            # read until matching \end{...}
            m = re.match(r"\\begin\{([^}*]+)", env)
            ename = m.group(1) if m else ""
            while i < len(lines):
                out.append(lines[i])
                if ename and lines[i].strip().startswith(f"\\end{{{ename}"):
                    i += 1
                    break
                i += 1
            out.append("")
            continue

        if line.strip().startswith("\\end{"):
            flush_para()
            out.append(line)
            i += 1
            continue

        # accumulate paragraph
        para_buf.append(line.strip())
        i += 1

    flush_para()
    # strip manuscript footer italics / orphaned markers
    text = "\n".join(out)
    text = re.sub(
        r"\\emph\{Manuscript[^}]*\}\s*",
        "",
        text,
    )
    text = re.sub(
        r"(?m)^\*Manuscript.*\*\s*$",
        "",
        text,
    )
    # drop empty lstlisting language=text when broken
    return text + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="Only convert this markdown filename")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    # figures symlink
    fig_link = ROOT / "book" / "latex" / "figures"
    fig_src = BOOK / "figures"
    if not fig_link.exists():
        try:
            fig_link.symlink_to(fig_src.resolve())
        except OSError:
            # copy not needed if relative works via graphicspath
            pass

    converted = 0
    for md_name, tex_base, kind in CHAPTERS:
        if args.only and args.only not in (md_name, tex_base):
            continue
        md_path = BOOK / md_name
        if not md_path.exists():
            print(f"skip missing {md_path}", file=sys.stderr)
            continue
        label = f"ch:{tex_base}"
        tex = convert_file(md_path, kind, label)
        out_path = OUT / f"{tex_base}.tex"
        out_path.write_text(tex, encoding="utf-8")
        print(f"wrote {out_path.relative_to(ROOT)} ({len(tex.splitlines())} lines)")
        converted += 1

    print(f"converted {converted} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
