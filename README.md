# JE Civil Prep (KRCL) — GitHub Pages

Bilingual (**English + ಕನ್ನಡ**) exam preparation site for **Konkan Railway Corporation Ltd**  
**Junior Engineer (Civil)** — Employment Notification **CO/P-R/02/2026**.

## Live site features

| Page | What it does |
|------|----------------|
| **Home** | Overview + exam snapshot |
| **Practice MCQs** | 500 topic-wise questions, instant feedback |
| **Full Mock** | Timed 90-min CBT mock (100 Q, +3/−1 scoring) |
| **Notes** | Browse study markdown in the browser |
| **PDFs** | View / download print-ready PDFs |

## Enable GitHub Pages

1. Create a new GitHub repository (example name: `je-civil-prep`).
2. Push this project (commands below).
3. On GitHub: **Settings → Pages**
   - **Source:** Deploy from a branch
   - **Branch:** `main`
   - **Folder:** `/docs`
4. Wait 1–2 minutes, then open:  
   `https://<your-username>.github.io/je-civil-prep/`

> Tip: keep the repo **public** if you want free Pages without a GitHub Pro plan.

## Push to GitHub (first time)

```bash
cd ~/Documents/JE_Civil_Exam_Prep
git init
git add .
git commit -m "Add JE Civil KRCL prep site with mocks, notes, and PDFs"
git branch -M main
git remote add origin https://github.com/<your-username>/je-civil-prep.git
git push -u origin main
```

Replace `<your-username>` and repo name as needed.

If `gh` CLI is installed:

```bash
gh repo create je-civil-prep --public --source=. --remote=origin --push
```

Then set Pages to **/docs** as above.

## Local preview

Do **not** open `docs/index.html` as a raw `file://` link (fetch will fail). Use a local server:

```bash
cd ~/Documents/JE_Civil_Exam_Prep/docs
python3 -m http.server 8080
```

Open: http://localhost:8080

## Rebuild quiz JSON (after editing MCQs)

```bash
python3 scripts/build_web_data.py
```

## Rebuild PDFs (optional)

```bash
python3 build_print_ready.py
cp *.pdf docs/pdfs/
```

## Exam pattern (JE Civil)

- **100 questions** · **90 minutes** · **3 marks each** · **−1** wrong  
- Science 10 · Maths 20 · GA/Reasoning 20 · **Technical 50**  
- Qualifying: UR/EWS **50%** · OBC/SC/ST **40%**

## Disclaimer

Personal study aid only. **Not affiliated** with Konkan Railway Corporation Ltd.  
Always verify details on the official site: [konkanrailway.com](https://www.konkanrailway.com)
