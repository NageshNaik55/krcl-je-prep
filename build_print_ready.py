#!/usr/bin/env python3
"""Build JE Civil PDFs with correct answers highlighted in green."""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

ROOT = Path("/Users/nageshnaik/Documents/JE_Civil_Exam_Prep")
BI = ROOT / "MCQs_Bilingual"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

NOTE_FILES = [
    "14_KRCL_Cheat_Sheet.md",
    "12_KRCL_Weighted_Study_Plan.md",
    "12B_90Min_Mock_Blueprint.md",
    "00_Overview_and_Study_Plan.md",
    "01_General_Science.md",
    "02_Basic_Mathematics.md",
    "03_GA_and_Reasoning.md",
    "04_Building_Materials.md",
    "05_Surveying_Levelling.md",
    "06_Mechanics_Structural.md",
    "07_Fluid_Hydraulics.md",
    "08_Geotech_Transportation.md",
    "09_Environmental_Estimation.md",
    "11_Formula_Sheet.md",
]

MCQ_FILES = sorted(BI.glob("*_EN_KN.md"))
MOCK_FILE = ROOT / "13_Full_Mock_JE_Civil_100Q.md"

# Also include older compact MCQs if present (for any leftover keys in notes)
OLD_MCQ = ROOT / "MCQs"


def md_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def convert_table(rows: list[str]) -> str:
    body = ["<table>"]
    for i, row in enumerate(rows):
        cols = [c.strip() for c in row.strip().strip("|").split("|")]
        if i == 1 and all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in cols):
            continue
        tag = "th" if i == 0 else "td"
        body.append("<tr>" + "".join(f"<{tag}>{md_inline(c)}</{tag}>" for c in cols) + "</tr>")
    body.append("</table>")
    return "\n".join(body)


def parse_answers(md: str) -> dict[int, str]:
    """Parse patterns like 1-b 2-a 10-c from answer key sections."""
    answers: dict[int, str] = {}
    # Prefer text after Answer Key heading
    key_blob = md
    m = re.search(r"(?:##\s*)?(?:ANSWER KEY|Answer Key).*", md, flags=re.I | re.S)
    if m:
        key_blob = m.group(0)
    for num, letter in re.findall(r"(?<!\d)(\d{1,3})\s*[-–—:.]\s*([a-dA-D])\b", key_blob):
        answers[int(num)] = letter.lower()
    return answers


def format_answer_chips(answers: dict[int, str], title: str = "") -> str:
    if not answers:
        return ""
    chips = []
    for n in sorted(answers):
        chips.append(
            f"<span class='chip'><b>Q{n}</b> → "
            f"<span class='chip-ans'>{answers[n].upper()}</span></span>"
        )
    head = f"<h3 class='ans-head'>{html.escape(title)}</h3>" if title else ""
    return (
        f"<div class='ans-box'>{head}"
        f"<p class='ans-label'>✅ Correct Answers | ಸರಿಯಾದ ಉತ್ತರಗಳು</p>"
        f"<div class='chip-row'>{''.join(chips)}</div></div>"
    )


def md_to_html(
    md: str,
    *,
    highlight_answers: bool = True,
    strip_answer_key_text: bool = False,
    answers: dict[int, str] | None = None,
) -> str:
    if answers is None:
        answers = parse_answers(md) if highlight_answers else {}

    working = md
    if strip_answer_key_text:
        working = re.split(r"\n##\s*Answer Key.*", working, maxsplit=1, flags=re.I)[0]
        working = re.split(r"\n##\s*ANSWER KEY.*", working, maxsplit=1, flags=re.I)[0]
        working = re.split(r"\n---\s*\n##\s*Answer.*", working, maxsplit=1, flags=re.I)[0]

    lines = working.splitlines()
    out: list[str] = []
    i = 0
    in_ul = False
    para: list[str] = []
    current_q: int | None = None

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + md_inline(" ".join(para)) + "</p>")
            para = []

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    while i < len(lines):
        line = lines[i]
        if "|" in line and i + 1 < len(lines) and re.search(r"\|?\s*:?-+:?\s*\|", lines[i + 1]):
            flush_para()
            close_ul()
            rows = []
            while i < len(lines) and "|" in lines[i]:
                rows.append(lines[i])
                i += 1
            out.append(convert_table(rows))
            continue

        if line.startswith("# "):
            flush_para()
            close_ul()
            out.append(f"<h1>{md_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            flush_para()
            close_ul()
            # Highlight answer-key headings
            title = line[3:]
            cls = " ans-head" if re.search(r"answer\s*key|ಉತ್ತರ", title, re.I) else ""
            out.append(f"<h2 class='{cls.strip()}'>{md_inline(title)}</h2>")
        elif line.startswith("### "):
            flush_para()
            close_ul()
            title = line[4:].strip()
            qm = re.match(r"Q\s*(\d+)", title, re.I)
            current_q = int(qm.group(1)) if qm else current_q
            badge = ""
            if highlight_answers and current_q in answers:
                badge = (
                    f" <span class='q-badge'>Answer: "
                    f"{answers[current_q].upper()}</span>"
                )
            out.append(f"<h3>{md_inline(title)}{badge}</h3>")
        elif line.strip() == "---":
            flush_para()
            close_ul()
            out.append("<hr/>")
        elif re.match(r"^\s*[-*]\s+", line):
            flush_para()
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{md_inline(re.sub(r'^\\s*[-*]\\s+', '', line))}</li>")
        elif re.match(r"^[a-dA-D]\)", line.strip()):
            flush_para()
            close_ul()
            opt_letter = line.strip()[0].lower()
            is_correct = (
                highlight_answers
                and current_q is not None
                and answers.get(current_q) == opt_letter
            )
            if is_correct:
                out.append(
                    f"<div class='opt correct'>"
                    f"<span class='tick'>✓</span> {md_inline(line.strip())}"
                    f" <span class='correct-tag'>CORRECT / ಸರಿ</span></div>"
                )
            else:
                out.append(f"<div class='opt'>{md_inline(line.strip())}</div>")
        elif line.strip() == "":
            flush_para()
            close_ul()
        else:
            close_ul()
            # Highlight inline answer-key lines like "1-b 2-a ..."
            if highlight_answers and re.search(r"\d+\s*[-–—]\s*[a-dA-D]", line):
                rendered = md_inline(line.strip())
                rendered = re.sub(
                    r"(\d{1,3}\s*[-–—]\s*[a-dA-D])",
                    r"<span class='inline-ans'>\1</span>",
                    rendered,
                    flags=re.I,
                )
                out.append(f"<p class='key-line'>{rendered}</p>")
            else:
                para.append(line.strip())
        i += 1

    flush_para()
    close_ul()

    # Append chip summary if we highlighted and had answers
    html_body = "\n".join(out)
    if highlight_answers and answers and strip_answer_key_text:
        html_body += format_answer_chips(answers)
    return html_body


CSS = """
@page { size: A4; margin: 12mm 10mm; }
:root { --ink:#1a1a1a; --muted:#444; --line:#ccc; --accent:#0b3d2e; --soft:#f4f7f5;
  --ans:#d8f5d0; --ans-border:#1b7a3d; --ans-text:#0d5c2e; --chip:#fff8c5; }
* { box-sizing: border-box; }
body { font-family: "Noto Sans Kannada", "Noto Sans", "Helvetica Neue", Arial, sans-serif;
  color:var(--ink); font-size:10pt; line-height:1.4; margin:0; background:#fff; }
.cover { page-break-after:always; min-height:88vh; padding:22mm 8mm; display:flex; flex-direction:column; justify-content:center;
  background: linear-gradient(160deg,#e8f2ec 0%,#fff 55%,#f7f3ea 100%); border-bottom:6px solid var(--accent); }
.cover h1 { font-size:24pt; color:var(--accent); margin:0 0 8px; line-height:1.2; }
.cover .kn { font-size:14pt; color:var(--muted); margin-bottom:18px; }
.section { page-break-before: always; }
h1 { font-size:14pt; color:var(--accent); border-bottom:2px solid var(--accent); padding-bottom:3px; margin-top:0; }
h2 { font-size:11.5pt; background:var(--soft); padding:3px 7px; border-left:4px solid var(--accent); margin-top:12px; }
h2.ans-head { background:var(--ans); border-left-color:var(--ans-border); color:var(--ans-text); }
h3 { font-size:10.5pt; margin:10px 0 4px; color:#123; }
p { margin:3px 0 6px; }
.opt { margin:2px 0 2px 8px; padding:2px 6px; border-radius:4px; }
.opt.correct {
  background: var(--ans) !important;
  border: 1.5px solid var(--ans-border);
  font-weight: 700;
  color: var(--ans-text);
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
.tick { color: var(--ans-border); font-weight: 900; margin-right: 4px; }
.correct-tag {
  display:inline-block; margin-left:6px; padding:1px 6px; border-radius:10px;
  background:#1b7a3d; color:#fff; font-size:8pt; font-weight:700;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.q-badge {
  display:inline-block; margin-left:8px; padding:1px 8px; border-radius:10px;
  background:#fff3a0; border:1px solid #c9a800; color:#5a4a00; font-size:9pt; font-weight:700;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.ans-box {
  margin:12px 0; padding:10px; background:var(--ans); border:2px solid var(--ans-border);
  border-radius:8px; -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.ans-label { font-weight:800; color:var(--ans-text); margin:0 0 8px; }
.ans-head { color:var(--ans-text); margin-top:0; }
.chip-row { display:flex; flex-wrap:wrap; gap:6px; }
.chip {
  display:inline-block; background:var(--chip); border:1px solid #c9a800;
  border-radius:6px; padding:3px 7px; font-size:9pt;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.chip-ans {
  display:inline-block; min-width:16px; text-align:center; font-weight:900;
  background:#1b7a3d; color:#fff; border-radius:4px; padding:0 5px;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.inline-ans {
  display:inline-block; background:#fff3a0; border:1px solid #1b7a3d;
  border-radius:4px; padding:0 4px; font-weight:800; color:#0d5c2e;
  margin:1px 2px; -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
.key-line { line-height: 1.9; }
ul { margin:4px 0 8px 16px; }
table { width:100%; border-collapse:collapse; margin:6px 0 10px; font-size:9pt; }
th,td { border:1px solid var(--line); padding:3px 5px; vertical-align:top; }
th { background:#e7eee9; text-align:left; }
hr { border:none; border-top:1px solid var(--line); margin:10px 0; }
@media print {
  .section { page-break-before: always; }
  a { color:inherit; text-decoration:none; }
  .opt.correct, .correct-tag, .q-badge, .ans-box, .chip, .chip-ans, .inline-ans {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
}
"""


def wrap(title: str, body: str) -> str:
    return f"""<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>
<title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>"""


def build_complete() -> Path:
    parts = ["""
    <section class='cover'>
      <h1>Junior Engineer (Civil)<br/>Complete Exam Preparation Guide</h1>
      <div class='kn'>ಜೂನಿಯರ್ ಎಂಜಿನಿಯರ್ (ಸಿವಿಲ್) — ಸಂಪೂರ್ಣ ಪರೀಕ್ಷಾ ತಯಾರಿ</div>
      <p><strong>Aligned to KRCL CO/P-R/02/2026</strong></p>
      <p>Correct answers are <span class='correct-tag'>CORRECT / ಸರಿ</span> highlighted in green.</p>
      <ul>
        <li>KRCL cheat sheet, weighted plan, mock blueprint</li>
        <li>Full syllabus notes + formula sheet</li>
        <li>500 bilingual MCQs + Full Mock #1 with highlighted answers</li>
      </ul>
    </section>
    """]
    for n in NOTE_FILES:
        text = (ROOT / n).read_text(encoding="utf-8")
        parts.append(
            f"<section class='section' id='{html.escape(n)}'>"
            f"{md_to_html(text, highlight_answers=True)}</section>"
        )
    parts.append(
        "<section class='section'><h1>PART B — Bilingual MCQs (50 each)</h1>"
        "<p>Green highlight = correct option. Yellow badge = answer letter.</p></section>"
    )
    for m in MCQ_FILES:
        text = m.read_text(encoding="utf-8")
        ans = parse_answers(text)
        parts.append(
            f"<section class='section'>"
            f"{md_to_html(text, highlight_answers=True, answers=ans)}"
            f"{format_answer_chips(ans, m.stem.replace('_', ' '))}"
            f"</section>"
        )
    if MOCK_FILE.exists():
        text = MOCK_FILE.read_text(encoding="utf-8")
        ans = parse_answers(text)
        parts.append(
            "<section class='section'><h1>PART C — Full Mock #1 (KRCL Pattern)</h1>"
            "<p>100 Q | Answers highlighted in green</p></section>"
        )
        parts.append(
            f"<section class='section'>"
            f"{md_to_html(text, highlight_answers=True, answers=ans)}"
            f"{format_answer_chips(ans, 'Full Mock #1')}"
            f"</section>"
        )
    out = ROOT / "JE_Civil_Complete_Print_Ready.html"
    out.write_text(wrap("JE Civil Complete Guide", "\n".join(parts)), encoding="utf-8")
    return out


def build_mcq_exam() -> Path:
    """Practice book WITH answers highlighted on each question (as requested)."""
    parts = ["""
    <section class='cover'>
      <h1>JE Civil — MCQ Practice Book</h1>
      <div class='kn'>MCQ ಅಭ್ಯಾಸ ಪುಸ್ತಕ — ಉತ್ತರಗಳು ಹೈಲೈಟ್</div>
      <p><strong>500 Questions</strong> | English + ಕನ್ನಡ</p>
      <p>Correct option marked with <span class='correct-tag'>CORRECT / ಸರಿ</span> green highlight.</p>
      <p>Each question also shows yellow <b>Answer: X</b> badge.</p>
    </section>
    """]
    for idx, m in enumerate(MCQ_FILES, 1):
        text = m.read_text(encoding="utf-8")
        title = m.stem.replace("_EN_KN", "").replace("_", " ")
        ans = parse_answers(text)
        parts.append(f"<section class='section'><h1>Set {idx:02d}. {html.escape(title)}</h1>")
        parts.append(
            md_to_html(
                text,
                highlight_answers=True,
                strip_answer_key_text=True,
                answers=ans,
            )
        )
        parts.append(format_answer_chips(ans, f"Set {idx:02d} Answer Key"))
        parts.append("</section>")
    out = ROOT / "JE_Civil_MCQ_Only_Exam_Practice.html"
    out.write_text(wrap("JE Civil MCQ Practice — Answers Highlighted", "\n".join(parts)), encoding="utf-8")
    return out


def build_full_mock() -> Path:
    text = MOCK_FILE.read_text(encoding="utf-8")
    ans = parse_answers(text)
    parts = ["""
    <section class='cover'>
      <h1>KRCL JE Civil — Full Mock #1</h1>
      <div class='kn'>ಪೂರ್ಣ ಮಾಕ್ #1 — ಉತ್ತರಗಳು ಹೈಲೈಟ್</div>
      <p><strong>90 minutes</strong> | 100 × 3 = <strong>300 marks</strong> | Negative −1</p>
      <p>Correct answers are highlighted in <b>green</b> with ✓ and yellow Answer badge.</p>
      <p>Tip: Cover the options with a paper strip if you want to self-test first.</p>
    </section>
    """,
    f"<section class='section'>"
    f"{md_to_html(text, highlight_answers=True, strip_answer_key_text=True, answers=ans)}"
    f"{format_answer_chips(ans, 'Full Mock #1 — Complete Answer Key')}"
    f"</section>",
    ]
    out = ROOT / "JE_Civil_Full_Mock_1_Exam.html"
    out.write_text(wrap("KRCL JE Civil Full Mock 1 — Answers Highlighted", "\n".join(parts)), encoding="utf-8")
    return out


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    # background-graphics / print colors via Chrome headless
    subprocess.run(
        [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        check=True,
        capture_output=True,
    )


def main():
    complete_html = build_complete()
    exam_html = build_mcq_exam()
    mock_html = build_full_mock()
    complete_pdf = ROOT / "JE_Civil_Complete_Print_Ready.pdf"
    exam_pdf = ROOT / "JE_Civil_MCQ_Only_Exam_Practice.pdf"
    mock_pdf = ROOT / "JE_Civil_Full_Mock_1_Exam.pdf"
    html_to_pdf(complete_html, complete_pdf)
    html_to_pdf(exam_html, exam_pdf)
    html_to_pdf(mock_html, mock_pdf)

    # Quick sanity: ensure highlight classes exist in HTML
    for p in (complete_html, exam_html, mock_html):
        t = p.read_text(encoding="utf-8")
        print(f"{p.name}: correct_opts={t.count('opt correct')} badges={t.count('q-badge')} chips={t.count('chip-ans')}")

    print("PDF:", complete_pdf, f"({complete_pdf.stat().st_size/1024/1024:.2f} MB)")
    print("PDF:", exam_pdf, f"({exam_pdf.stat().st_size/1024/1024:.2f} MB)")
    print("PDF:", mock_pdf, f"({mock_pdf.stat().st_size/1024/1024:.2f} MB)")


if __name__ == "__main__":
    main()
