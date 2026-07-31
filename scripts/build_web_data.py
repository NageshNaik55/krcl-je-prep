#!/usr/bin/env python3
"""Convert bilingual MCQ markdown + full mock into JSON for the web app."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("/Users/nageshnaik/Documents/JE_Civil_Exam_Prep")
BI = ROOT / "MCQs_Bilingual"
MOCK = ROOT / "13_Full_Mock_JE_Civil_100Q.md"
OUT = ROOT / "docs" / "data"


def parse_answers(md: str) -> dict[int, str]:
    answers: dict[int, str] = {}
    m = re.search(r"(?:##\s*)?(?:ANSWER KEY|Answer Key).*", md, flags=re.I | re.S)
    blob = m.group(0) if m else md
    for num, letter in re.findall(r"(?<!\d)(\d{1,3})\s*[-–—:.]\s*([a-dA-D])\b", blob):
        answers[int(num)] = letter.lower()
    return answers


def parse_questions(md: str) -> list[dict]:
    answers = parse_answers(md)
    # strip answer key for question parsing
    body = re.split(r"\n##\s*(?:ANSWER KEY|Answer Key).*", md, maxsplit=1, flags=re.I)[0]
    blocks = re.split(r"\n(?=###\s*Q\d+)", body)
    questions = []
    for block in blocks:
        hm = re.match(r"###\s*Q(\d+)\s*", block)
        if not hm:
            continue
        qid = int(hm.group(1))
        en = ""
        kn = ""
        em = re.search(r"\*\*EN:\*\*\s*(.+)", block)
        km = re.search(r"\*\*KN:\*\*\s*(.+)", block)
        if em:
            en = em.group(1).strip()
        if km:
            kn = km.group(1).strip()
        # Sometimes EN and KN on same line in mock
        if not en and not kn:
            both = re.search(r"\*\*EN:\*\*\s*(.+?)\s*\*\*KN:\*\*\s*(.+)", block)
            if both:
                en, kn = both.group(1).strip(), both.group(2).strip()
        options = {}
        for letter, text in re.findall(r"^([a-dA-D])\)\s*(.+)$", block, flags=re.M):
            options[letter.lower()] = text.strip()
        if len(options) < 4:
            continue
        questions.append(
            {
                "id": qid,
                "en": en,
                "kn": kn,
                "options": options,
                "answer": answers.get(qid, ""),
            }
        )
    return questions


TOPIC_META = [
    ("01_Science_50_EN_KN.md", "science", "General Science", "ಸಾಮಾನ್ಯ ವಿಜ್ಞಾನ", 10),
    ("02_Mathematics_50_EN_KN.md", "maths", "Basic Mathematics", "ಮೂಲಭೂತ ಗಣಿತ", 20),
    ("03_General_Awareness_50_EN_KN.md", "ga", "General Awareness", "ಸಾಮಾನ್ಯ ಜ್ಞಾನ", 20),
    ("04_Reasoning_50_EN_KN.md", "reasoning", "Reasoning", "ತರ್ಕಶಕ್ತಿ", 20),
    ("05_Building_Materials_50_EN_KN.md", "materials", "Building Materials", "ಕಟ್ಟಡ ಸಾಮಗ್ರಿ", 50),
    ("06_Surveying_50_EN_KN.md", "survey", "Surveying", "ಸಮೀಕ್ಷೆ", 50),
    ("07_Mechanics_Structural_50_EN_KN.md", "structures", "Mechanics & Structures", "ರಚನಾ ಎಂಜಿನಿಯರಿಂಗ್", 50),
    ("08_Fluid_Hydraulics_50_EN_KN.md", "fluids", "Fluid Mechanics", "ದ್ರವ ಯಾಂತ್ರಿಕತೆ", 50),
    ("09_Geotech_Transportation_50_EN_KN.md", "geotech", "Geotech & Transport", "ಭೂತಾಂತ್ರಿಕ / ಸಾರಿಗೆ", 50),
    ("10_Environmental_Estimation_50_EN_KN.md", "env", "Environment & Estimation", "ಪರಿಸರ / ಅಂದಾಜು", 50),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "topics").mkdir(exist_ok=True)
    index = []
    for fname, slug, title_en, title_kn, weight in TOPIC_META:
        path = BI / fname
        qs = parse_questions(path.read_text(encoding="utf-8"))
        data = {
            "id": slug,
            "title_en": title_en,
            "title_kn": title_kn,
            "count": len(qs),
            "exam_weight_hint": weight,
            "questions": qs,
        }
        (OUT / "topics" / f"{slug}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        index.append(
            {
                "id": slug,
                "title_en": title_en,
                "title_kn": title_kn,
                "count": len(qs),
                "file": f"topics/{slug}.json",
            }
        )
        print(f"{slug}: {len(qs)} Q")

    (OUT / "topics.json").write_text(
        json.dumps({"topics": index}, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    mock_qs = parse_questions(MOCK.read_text(encoding="utf-8"))
    mock = {
        "id": "full-mock-1",
        "title_en": "KRCL JE Civil — Full Mock #1",
        "title_kn": "ಪೂರ್ಣ ಮಾಕ್ ಪರೀಕ್ಷೆ #1",
        "duration_sec": 90 * 60,
        "marks_per_q": 3,
        "negative": 1,
        "total_questions": len(mock_qs),
        "sections": [
            {"name": "General Science", "from": 1, "to": 10},
            {"name": "Basic Mathematics", "from": 11, "to": 30},
            {"name": "GA & Reasoning", "from": 31, "to": 50},
            {"name": "Technical Ability", "from": 51, "to": 100},
        ],
        "questions": mock_qs,
    }
    (OUT / "mock1.json").write_text(
        json.dumps(mock, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"mock1: {len(mock_qs)} Q")

    notes = []
    notes_dir = ROOT / "docs" / "notes"
    for p in sorted(notes_dir.glob("*.md")):
        notes.append({"file": p.name, "title": p.stem.replace("_", " ")})
    (OUT / "notes.json").write_text(
        json.dumps({"notes": notes}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"notes: {len(notes)}")


if __name__ == "__main__":
    main()
