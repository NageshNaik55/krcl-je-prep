/* Shared helpers for JE Civil Pages site */
window.JE = {
  async fetchJSON(rel) {
    const path = rel.startsWith("./") ? rel : `./${rel}`;
    const res = await fetch(path);
    if (!res.ok) throw new Error(`Failed to load ${rel} (${res.status})`);
    return res.json();
  },

  score({ correct, wrong, marks = 3, neg = 1 }) {
    return correct * marks - wrong * neg;
  },

  formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  },

  setActiveNav() {
    const file = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".nav-links a").forEach((a) => {
      const href = (a.getAttribute("href") || "").split("/").pop();
      if (href === file || ((file === "" || file === "docs") && href === "index.html")) {
        a.classList.add("active");
      }
    });
  },
};

document.addEventListener("DOMContentLoaded", () => window.JE.setActiveNav());
