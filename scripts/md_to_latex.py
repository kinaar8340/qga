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


def normalize_unicode(s: str) -> str:
    """Map common Unicode punctuation to ASCII/LaTeX-friendly forms.

    Curly double quotes must NOT become backticks: that confuses inline-code
    extraction and can swallow whole sentences (including math) into \\texttt.
    """
    pairs = {
        "\u2014": "---",
        "\u2013": "--",
        # Keep straight apostrophe; curly singles → ASCII apostrophe
        "\u2018": "'",
        "\u2019": "'",
        # Placeholder double quotes (converted to `` '' in text chunks only)
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u2192": "\\(\\rightarrow\\)",
        "\u21a6": "\\(\\mapsto\\)",
        "\u2190": "\\(\\leftarrow\\)",
        "\u2194": "\\(\\leftrightarrow\\)",
        "\u00d7": "\\(\\times\\)",
        "\u2212": "-",
        "\u2248": "\\(\\approx\\)",
        "\u2260": "\\(\\neq\\)",
        "\u2264": "\\(\\leq\\)",
        "\u2265": "\\(\\geq\\)",
        "\u00b7": "\\(\\cdot\\)",
        "\u221e": "\\(\\infty\\)",
        "\u21d2": "\\(\\Rightarrow\\)",
        "\u2261": "\\(\\equiv\\)",
        "\ufffd": "",
    }
    for a, b in pairs.items():
        s = s.replace(a, b)
    s = "".join(ch if ord(ch) < 128 else "?" for ch in s)
    return s


def escape_text(s: str) -> str:
    """Escape LaTeX specials outside math."""
    s = normalize_unicode(s)
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
    escaped = escape_text(content)
    for ch, repl in (
        ("/", r"/\allowbreak{}"),
        (".", r".\allowbreak{}"),
        (":", r":\allowbreak{}"),
        (r"\_", r"\_\allowbreak{}"),
        (r"\textasciitilde{}", r"\textasciitilde{}\allowbreak{}"),
    ):
        escaped = escaped.replace(ch, repl)
    return r"\texttt{" + escaped + "}"


def convert_inline(s: str) -> str:
    r"""Convert inline markdown; leave \( \) and existing math alone."""
    s = normalize_unicode(s)
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
    pos = 0
    chunks: list[str] = []
    for m in pattern.finditer(s):
        if m.start() > pos:
            chunks.append(("text", s[pos : m.start()]))
        tok = m.group(0)
        if tok.startswith("[") and "](" in tok:
            chunks.append(("link", tok))
        elif tok.startswith("`"):
            chunks.append(("code", tok[1:-1]))
        elif tok.startswith("$$"):
            chunks.append(("dmath", tok[2:-2]))
        elif tok.startswith("\\["):
            chunks.append(("dmath", tok[2:-2]))
        elif tok.startswith("\\("):
            chunks.append(("imath", tok[2:-2]))
        elif tok.startswith("$"):
            chunks.append(("imath", tok[1:-1]))
        elif tok.startswith("http"):
            chunks.append(("url", tok.rstrip(".,;:)")))
        else:
            chunks.append(("text", tok))
        pos = m.end()
    if pos < len(s):
        chunks.append(("text", s[pos:]))

    def format_text_chunk(content: str) -> str:
        t = latex_quotes(content)
        # bold **...**
        t = re.sub(
            r"\*\*(.+?)\*\*",
            lambda m: r"\textbf{" + escape_text(m.group(1)) + "}",
            t,
        )
        # italic *...* (avoid bold leftovers)
        t = re.sub(
            r"(?<!\*)\*([^*]+?)\*(?!\*)",
            lambda m: r"\emph{" + escape_text(m.group(1)) + "}",
            t,
        )
        # remaining text escape — but don't escape already-inserted commands
        pieces = re.split(r"(\\(?:textbf|emph)\{[^}]*\})", t)
        rebuilt = []
        for p in pieces:
            if p.startswith("\\textbf") or p.startswith("\\emph"):
                rebuilt.append(p)
            else:
                rebuilt.append(escape_text(p))
        return "".join(rebuilt)

    out = []
    for kind, content in chunks:
        if kind == "text":
            out.append(format_text_chunk(content))
        elif kind == "link":
            lm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", content)
            if not lm:
                out.append(format_text_chunk(content))
                continue
            label_raw, url = lm.group(1), lm.group(2)
            # Label may contain `code`, **bold**, math — recurse lightly
            label_tex = convert_inline(label_raw) if ("`" in label_raw or "*" in label_raw or "\\" in label_raw) else escape_text(label_raw)
            url_tex = url.replace("%", r"\%").replace("#", r"\#")
            out.append(rf"\href{{{url_tex}}}{{{label_tex}}}")
        elif kind == "code":
            out.append(latex_code_span(content))
        elif kind == "url":
            # xurl/hyperref: breakable URL (no manual escape)
            safe = content.replace("%", r"\%").replace("#", r"\#")
            out.append(r"\url{" + safe + "}")
        elif kind == "imath":
            out.append(r"\(" + content + r"\)")
        elif kind == "dmath":
            out.append("\n\\[\n" + content.strip() + "\n\\]\n")
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
    if ncols == 1:
        colspec = X
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
        # figure caption lines like *Figure 1.1.* ...
        m = re.match(r"^\*(Figure|Auxiliary Figure) ([^*]+)\.\*\s*(.*)$", text)
        if m:
            # already handled with image usually; emit as caption continuation if orphan
            out.append(r"\begin{quote}\small\textit{" + convert_inline(text.strip("*")) + r"}\end{quote}")
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
                raw = "\n".join(code_buf)
                raw = (
                    raw.replace("→", "->")
                    .replace("←", "<-")
                    .replace("↦", "|->")
                    .replace("—", "--")
                    .replace("–", "-")
                    .replace("\u2018", "'")
                    .replace("\u2019", "'")
                    .replace("\u201c", '"')
                    .replace("\u201d", '"')
                )
                raw = "".join(ch if ord(ch) < 128 else "?" for ch in raw)
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
            # caption from following italic line if present
            caption = alt
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("*"):
                cap_line = lines[i + 1].strip().strip("*")
                caption = cap_line
                i += 1
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
            # strip trailing markdown emphasis
            title_tex = convert_inline(title)
            if level == 1:
                if first_heading:
                    first_heading = False
                    plain = escape_text(re.sub(r"\*\*|__|`", "", title))
                    if kind == "front":
                        out.append(rf"\chapter*{{{title_tex}}}")
                        out.append(rf"\label{{{label_base}}}")
                        out.append(rf"\addcontentsline{{toc}}{{chapter}}{{{plain}}}")
                        out.append(rf"\markboth{{{plain}}}{{}}")
                    elif kind == "appendix":
                        # Title already contains "Appendix A — ..."; book class will prefix "Appendix A"
                        # Strip leading "Appendix X — " to avoid "Appendix A Appendix A — ..."
                        short = re.sub(
                            r"^Appendix\s+[A-Z]\s*[\u2014\u2013—–-]+\s*",
                            "",
                            title,
                            flags=re.I,
                        )
                        short_tex = convert_inline(short)
                        out.append(rf"\chapter{{{short_tex}}}")
                        out.append(rf"\label{{{label_base}}}")
                    else:
                        out.append(rf"\chapter{{{title_tex}}}")
                        out.append(rf"\label{{{label_base}}}")
                else:
                    out.append(rf"\section*{{{title_tex}}}")
            elif level == 2:
                lab = f"{label_base}:{slugify(title)}"
                out.append(rf"\section{{{title_tex}}}")
                out.append(rf"\label{{{lab}}}")
            elif level == 3:
                lab = f"{label_base}:{slugify(title)}"
                out.append(rf"\subsection{{{title_tex}}}")
                out.append(rf"\label{{{lab}}}")
            else:
                out.append(rf"\subsubsection{{{title_tex}}}")
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
