/**
 * Interactive quiz engine for topic practice + full mock.
 * Modes:
 *  - practice: show correct after each (optional), no hard timer
 *  - mock: timed, hide answers until submit
 */
(function () {
  function createQuiz(config) {
    const {
      root,
      questions,
      mode = "practice", // practice | mock
      durationSec = null,
      marksPerQ = 3,
      negative = 1,
      title = "Quiz",
      onComplete = null,
    } = config;

    let idx = 0;
    let lang = localStorage.getItem("je-lang") || "both"; // en | kn | both
    const answers = {}; // id -> selected letter
    const flagged = new Set();
    let remaining = durationSec;
    let timerId = null;
    let finished = false;
    let revealMode = mode === "practice"; // reveal after select in practice

    root.innerHTML = `
      <div class="quiz-shell">
        <aside class="quiz-side">
          <div class="panel">
            <h3>${escapeHtml(title)}</h3>
            <div class="muted" id="q-progress">Question 1 / ${questions.length}</div>
            <div class="progress-bar"><span id="q-bar"></span></div>
            ${
              durationSec
                ? `<div class="muted">Time left</div><div class="timer" id="q-timer">${JE.formatTime(
                    durationSec
                  )}</div>`
                : ""
            }
            <div style="margin-top:0.8rem">
              <div class="muted" style="margin-bottom:0.35rem">Language</div>
              <div class="lang-toggle" id="lang-toggle">
                <button type="button" data-lang="en">EN</button>
                <button type="button" data-lang="kn">ಕನ್ನಡ</button>
                <button type="button" data-lang="both">Both</button>
              </div>
            </div>
            <div class="nav-q" id="q-nav"></div>
            <div style="margin-top:0.9rem; display:grid; gap:0.45rem">
              <button class="btn btn-secondary" type="button" id="btn-flag">Flag question</button>
              <button class="btn btn-primary" type="button" id="btn-submit">${
                mode === "mock" ? "Submit Mock" : "Finish & Score"
              }</button>
            </div>
          </div>
        </aside>
        <main class="panel" id="q-main"></main>
      </div>
      <section class="panel hidden" id="q-results" style="margin-top:1rem"></section>
    `;

    const main = root.querySelector("#q-main");
    const nav = root.querySelector("#q-nav");
    const bar = root.querySelector("#q-bar");
    const progress = root.querySelector("#q-progress");
    const timerEl = root.querySelector("#q-timer");
    const results = root.querySelector("#q-results");

    function escapeHtml(s) {
      return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
    }

    function syncLangButtons() {
      root.querySelectorAll("#lang-toggle button").forEach((b) => {
        b.classList.toggle("on", b.dataset.lang === lang);
      });
    }

    function renderNav() {
      nav.innerHTML = questions
        .map((q, i) => {
          const classes = [
            i === idx ? "current" : "",
            answers[q.id] ? "done" : "",
            flagged.has(q.id) ? "flag" : "",
          ]
            .filter(Boolean)
            .join(" ");
          return `<button type="button" data-i="${i}" class="${classes}">${i + 1}</button>`;
        })
        .join("");
    }

    function renderQuestion() {
      if (finished) return;
      const q = questions[idx];
      const selected = answers[q.id];
      progress.textContent = `Question ${idx + 1} / ${questions.length}`;
      bar.style.width = `${((idx + 1) / questions.length) * 100}%`;

      const showEn = lang === "en" || lang === "both";
      const showKn = lang === "kn" || lang === "both";

      let feedback = "";
      if (revealMode && selected) {
        const ok = selected === q.answer;
        feedback = ok
          ? `<div class="alert" style="background:#e8f7ec;border-color:#1b7a3d;color:#0d5c2e">✓ Correct — Answer is <b>${q.answer.toUpperCase()}</b></div>`
          : `<div class="alert" style="background:#fdecea;border-color:#a61e1e;color:#7a1212">✗ Wrong — Correct answer is <b>${q.answer.toUpperCase()}</b></div>`;
      }

      main.innerHTML = `
        <div class="q-meta">
          <span class="pill">Q${q.id}</span>
          ${flagged.has(q.id) ? `<span class="tag">Flagged</span>` : ""}
          ${mode === "mock" ? `<span class="pill">+${marksPerQ} / −${negative}</span>` : ""}
        </div>
        ${showEn ? `<p class="q-text">${escapeHtml(q.en)}</p>` : ""}
        ${showKn ? `<p class="q-kn">${escapeHtml(q.kn)}</p>` : ""}
        <div class="options">
          ${["a", "b", "c", "d"]
            .map((letter) => {
              const text = q.options[letter] || "";
              let cls = "option";
              if (selected === letter) cls += " selected";
              if (revealMode && selected) {
                if (letter === q.answer) cls += " correct";
                else if (letter === selected) cls += " wrong";
              }
              return `<button type="button" class="${cls}" data-opt="${letter}">
                <span class="letter">${letter.toUpperCase()}</span>${escapeHtml(text)}
              </button>`;
            })
            .join("")}
        </div>
        ${feedback}
        <div class="quiz-actions">
          <button class="btn btn-secondary" type="button" id="btn-prev" ${
            idx === 0 ? "disabled" : ""
          }>Previous</button>
          <button class="btn btn-primary" type="button" id="btn-next">${
            idx === questions.length - 1 ? "Review / Finish" : "Next"
          }</button>
        </div>
      `;

      main.querySelectorAll(".option").forEach((btn) => {
        btn.addEventListener("click", () => {
          if (finished) return;
          answers[q.id] = btn.dataset.opt;
          renderNav();
          renderQuestion();
        });
      });
      main.querySelector("#btn-prev")?.addEventListener("click", () => {
        idx = Math.max(0, idx - 1);
        renderNav();
        renderQuestion();
      });
      main.querySelector("#btn-next")?.addEventListener("click", () => {
        if (idx === questions.length - 1) {
          // jump to submit confirmation visually
          root.querySelector("#btn-submit").focus();
          return;
        }
        idx = Math.min(questions.length - 1, idx + 1);
        renderNav();
        renderQuestion();
      });
      renderNav();
    }

    function compute() {
      let correct = 0;
      let wrong = 0;
      let skipped = 0;
      questions.forEach((q) => {
        const a = answers[q.id];
        if (!a) skipped += 1;
        else if (a === q.answer) correct += 1;
        else wrong += 1;
      });
      const score = JE.score({ correct, wrong, marks: marksPerQ, neg: negative });
      const max = questions.length * marksPerQ;
      return { correct, wrong, skipped, score, max, pct: max ? Math.round((score / max) * 1000) / 10 : 0 };
    }

    function finish() {
      if (finished) return;
      finished = true;
      if (timerId) clearInterval(timerId);
      const r = compute();
      results.classList.remove("hidden");
      results.innerHTML = `
        <h2>Result | ಫಲಿತಾಂಶ</h2>
        <div class="results-grid">
          <div class="result-card"><b>${r.score}</b><span class="muted">Score / ${r.max}</span></div>
          <div class="result-card"><b>${r.correct}</b><span class="muted">Correct</span></div>
          <div class="result-card"><b>${r.wrong}</b><span class="muted">Wrong (−${negative} each)</span></div>
          <div class="result-card"><b>${r.skipped}</b><span class="muted">Skipped</span></div>
          <div class="result-card"><b>${r.pct}%</b><span class="muted">Percentage</span></div>
        </div>
        <p class="muted">Formula used: Score = ${marksPerQ}×Correct − ${negative}×Wrong (KRCL pattern).</p>
        <p><b>UR qualifying reference:</b> 50% &nbsp;|&nbsp; <b>Practice target:</b> 70%+</p>
        <div style="margin-top:0.8rem; display:flex; gap:0.5rem; flex-wrap:wrap">
          <button class="btn btn-secondary" type="button" id="btn-review">Review answers</button>
          <button class="btn btn-primary" type="button" id="btn-retry">Retry</button>
        </div>
        <div id="review-list" class="hidden" style="margin-top:1rem"></div>
      `;
      results.querySelector("#btn-review").addEventListener("click", () => {
        const box = results.querySelector("#review-list");
        box.classList.toggle("hidden");
        box.innerHTML = questions
          .map((q) => {
            const a = answers[q.id];
            const ok = a && a === q.answer;
            return `<div style="padding:0.55rem 0; border-bottom:1px solid var(--line)">
              <b>Q${q.id}</b> — Your: <b>${(a || "—").toUpperCase()}</b> |
              Correct: <b style="color:var(--good)">${q.answer.toUpperCase()}</b>
              ${ok ? "✓" : "✗"}
              <div class="muted">${escapeHtml(q.en)}</div>
            </div>`;
          })
          .join("");
      });
      results.querySelector("#btn-retry").addEventListener("click", () => location.reload());
      results.scrollIntoView({ behavior: "smooth", block: "start" });
      revealMode = true;
      renderQuestion();
      if (onComplete) onComplete(r);
    }

    root.querySelector("#btn-flag").addEventListener("click", () => {
      const id = questions[idx].id;
      if (flagged.has(id)) flagged.delete(id);
      else flagged.add(id);
      renderQuestion();
    });
    root.querySelector("#btn-submit").addEventListener("click", () => {
      const r = compute();
      const unanswered = r.skipped;
      const msg =
        unanswered > 0
          ? `You have ${unanswered} unanswered questions. Submit anyway?`
          : "Submit and see your score?";
      if (confirm(msg)) finish();
    });
    nav.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-i]");
      if (!btn) return;
      idx = Number(btn.dataset.i);
      renderQuestion();
    });
    root.querySelector("#lang-toggle").addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-lang]");
      if (!btn) return;
      lang = btn.dataset.lang;
      localStorage.setItem("je-lang", lang);
      syncLangButtons();
      renderQuestion();
    });

    if (durationSec && timerEl) {
      timerId = setInterval(() => {
        remaining -= 1;
        timerEl.textContent = JE.formatTime(Math.max(0, remaining));
        timerEl.classList.toggle("warn", remaining <= 15 * 60);
        timerEl.classList.toggle("danger", remaining <= 5 * 60);
        if (remaining <= 0) {
          clearInterval(timerId);
          alert("Time is up! Submitting your mock.");
          finish();
        }
      }, 1000);
    }

    syncLangButtons();
    renderQuestion();
  }

  window.createQuiz = createQuiz;
})();
