/* ValhallaRaces compendium — shared app logic.
   Handles: data loading + caching, card rendering, live search,
   group filters, and the detail modal with buff/debuff columns. */

(() => {
  "use strict";

  const DATA_URL = "assets/data/data.json";
  const ENCHANT_URL = "assets/data/enchantments.json";
  const COMBO_URL = "assets/data/combos.json";

  const el = (sel, root = document) => root.querySelector(sel);
  const els = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* ---- icon rendering ---- */

  function customKeys() {
    try { return window.ICONS && window.ICONS._custom && window.ICONS._custom.length ? window.ICONS._custom : null; }
    catch (e) { return null; }
  }

  function monogramOf(key) {
    // Build a two-letter monogram from the snake_case key (e.g. "fire_elemental" -> "FE")
    const clean = key.replace(/[_-]+/g, " ").replace(/\d+/g, " ").replace(/\s+/g, " ").trim();
    const words = clean.split(" ");
    let letters = "";
    const first = (words[0] || "?").charAt(0);
    const second = words.length > 1 ? (words[1] || "").charAt(0) : "";
    letters = (first + second).toUpperCase();
    if (!letters) letters = key.charAt(0).toUpperCase() || "?";
    return letters;
  }

  function iconSVG(key, size = 64) {
    const custom = customKeys();
    // Use a hand-drawn icon when the key is listed as custom.
    if (custom) {
      if (custom.includes(key) && window.ICONS[key]) {
        const inner = window.ICONS[key];
        return `<svg viewBox="0 0 64 64" width="${size}" height="${size}" fill="none"
          stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
          aria-hidden="true">${inner}</svg>`;
      }
    } else {
      const inner = (window.ICONS && ICONS[key]) || "";
      if (inner) {
        return `<svg viewBox="0 0 64 64" width="${size}" height="${size}" fill="none"
          stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
          aria-hidden="true">${inner}</svg>`;
      }
    }
    // Fallback: monogram letter glyph
    const letters = monogramOf(key);
    const displaySize = size > 100 ? "lg" : "sm";
    return `<span class="icon-mono icon-mono--${displaySize}" aria-hidden="true">${letters}</span>`;
  }

  /* ---- model helpers ---- */

  function brittleness(stats) {
    return stats.reduce((acc, s) =>
      s.kind === "buff" && s.key !== "SCALE" ? acc + Math.abs(s.value) : acc, 0);
  }

  function cardPM(stats) {
    return stats.reduce((acc, s) =>
      s.kind === "debuff" && s.key !== "SCALE" ? acc + Math.abs(s.value) : acc, 0);
  }

  function flavorOf(desc) {
    // Strip the divider and everything after "benefit from"; keep the intro prose.
    const idx = desc.findIndex((l) => /benefit from/i.test(l));
    const head = idx >= 0 ? desc.slice(0, idx) : desc;
    const text = head
      .join(" ")
      .replace(/\s+/g, " ")
      .trim();
    return text || "No prose recorded for this entry.";
  }

  function statFriendly(stat) {
    const sign = stat.magnitude % 1 === 0 ? "" : "";
    const num = Number.isInteger(stat.magnitude)
      ? String(stat.magnitude)
      : stat.magnitude.toFixed(1);
    const unit = stat.percent ? "%" : "";
    const prefix = stat.kind === "buff" ? "+" : "–";
    return `${prefix}${num}${unit}`;
  }

  /* ---- card rendering ---- */

  function cardFor(item, type) {
    const buffs = item.stats.filter((s) => s.kind === "buff");
    const debuffs = item.stats.filter((s) => s.kind === "debuff");
    const groupName = item.group_name ? item.group_name : "";

    const b = brittleness(item.stats);
    const p = cardPM(item.stats);
    const stripe = `linear-gradient(90deg,
      rgba(87,192,122,.55) 0%,
      rgba(87,192,122,.55) ${b}%,
      transparent ${b + 4}%,
      transparent ${92 - p}%,
      rgba(223,93,93,.55) ${92 - p}%,
      rgba(223,93,93,.55) 100%)`;

    return `
      <button class="card" data-key="${item.key}" data-type="${type}"
        data-search="${(item.name + " " + groupName + " " + (item.prefix || "")).toLowerCase()}">
        <span class="card-stripe" style="background:${stripe};height:3px;display:block;border-radius:0"></span>
        <div class="card-top">
          <span class="card-kind">${type === "race" ? "Race" : "Class"}</span>
          ${groupName ? `<span class="card-group">${groupName}</span>` : ""}
        </div>
        <div class="card-icon">${iconSVG(item.key)}</div>
        <h3 class="card-name">${item.name}</h3>
        <p class="card-blurb">${flavorOf(item.description)}</p>
        <div class="card-color" style="background:${stripe}"></div>
      </button>`;
  }

  function renderGrid(container, items, type, { sections = false } = {}) {
    if (sections) {
      let html = "";
      const groups = [...new Set(items.map((i) => i.group).filter(Boolean))].sort((a, b) => a - b);
      for (const g of groups) {
        const label = (items.find((i) => i.group === g) || {}).group_name || ("Group " + g);
        html += `<div class="group-section">
          <h2 class="group-head">${g ? `Group ${g} · ` : ""}${label}</h2>
          <div class="group-grid">`;
        for (const it of items.filter((i) => i.group === g)) {
          html += cardFor(it, type);
        }
        html += `</div></div>`;
      }
      container.innerHTML = html;
      return;
    }
    container.innerHTML = items.map((it) => cardFor(it, type)).join("");
  }

  /* ---- search + filter state ---- */

  function applyFilters({ grid, items, type, searchInput, activeFilter, match }) {
    const q = (searchInput ? searchInput.value : "").trim().toLowerCase();
    const cards = els(".card", grid);

    for (const card of cards) {
      const key = card.dataset.key;
      const item = items.find((i) => i.key === key);
      let show = true;
      if (match) {
        show = match({ item, card, q, activeFilter });
      } else {
        const matchesSearch =
          !q ||
          card.dataset.search.includes(q) ||
          item.stats.some((s) => s.label.toLowerCase().includes(q));
        const inGroup = !activeFilter || String(item.group) === activeFilter;
        show = matchesSearch && inGroup;
      }
      card.style.display = show ? "" : "none";
    }

    // Collapse empty group sections (classes grouped view)
    for (const sec of els(".group-section", grid)) {
      const any = els(".card", sec).some((c) => c.style.display !== "none");
      sec.style.display = any ? "" : "none";
    }

    const visible = cards.filter((c) => c.style.display !== "none").length;
    const pageNode = grid.closest("[data-page]");
    const countEl = pageNode ? el(".live-count", pageNode) : null;
    if (countEl) countEl.textContent = `${visible} / ${items.length}`;

    let node = el(".no-results", grid.parentElement);
    if (visible === 0) {
      if (!node) {
        node = document.createElement("div");
        node.className = "no-results";
        node.id = "no-results";
        grid.after(node);
      }
      node.textContent =
        activeFilter
          ? `Nothing in ${activeFilter} matches “${q}”.`
          : q
            ? `No entry matches “${q}”.`
            : "Nothing to show.";
    } else if (node) {
      node.remove();
    }
  }

  /* ---- enchant rendering ---- */

  function enchantChips(arr) {
    return arr && arr.length ? arr.map((s) => `<span class="chip">${s}</span>`).join(" ") : "";
  }

  function enchantCardFor(en) {
    return `
      <button class="card enchant-card" data-key="${en.key}" data-type="enchant"
        data-search="${(en.name + " " + en.category + " " + en.summary).toLowerCase()}">
        <span class="card-stripe" style="background:linear-gradient(90deg,var(--brass),var(--brass-bright));height:3px;display:block;border-radius:0"></span>
        <div class="card-top">
          <span class="card-kind">Enchantment</span>
          <span class="card-group">${en.category}</span>
        </div>
        <div class="card-icon">${iconSVG(en.key)}</div>
        <h3 class="card-name">${en.name}</h3>
        <p class="card-blurb">${en.summary}</p>
        <div class="enchant-meta">
          <span class="meta-cell"><em>Max</em>${en.max_level}</span>
          <span class="meta-cell"><em>Weight</em>${en.weight}</span>
        </div>
      </button>`;
  }

  function openEnchantModal(en) {
    lastFocus = document.activeElement;
    const scrim = document.createElement("div");
    scrim.className = "modal-scrim";
    scrim.innerHTML = `
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <button class="modal-close" aria-label="Close">✕
          <svg><path d="M6 6 L18 18 M18 6 L6 18"/></svg>
        </button>
        <div class="modal-hero">
          <div class="modal-icon">${iconSVG(en.key, 132)}</div>
          <div>
            <div class="modal-prefix">${en.category}</div>
            <h2 class="modal-title" id="modal-title">${en.name}</h2>
            <div class="modal-kind">Enchantment</div>
          </div>
        </div>
        <div class="modal-body">
          <p class="modal-flavor">${en.summary}</p>
          <div class="enchant-detail">
            <div class="detail-row"><span class="detail-label">Max Level</span><span class="detail-val">${en.max_level}</span></div>
            <div class="detail-row"><span class="detail-label">Weight</span><span class="detail-val">${en.weight}</span></div>
            ${en.incompatible && en.incompatible.length ? `<div class="detail-row"><span class="detail-label">Incompatible With</span><span class="detail-val">${enchantChips(en.incompatible)}</span></div>` : ""}
            ${en.primary && en.primary.length ? `<div class="detail-row"><span class="detail-label">Primary Items</span><span class="detail-val">${enchantChips(en.primary)}</span></div>` : ""}
            ${en.secondary && en.secondary.length ? `<div class="detail-row"><span class="detail-label">Secondary Items</span><span class="detail-val">${enchantChips(en.secondary)}</span></div>` : ""}
          </div>
        </div>
      </section>`;

    document.body.appendChild(scrim);
    document.body.classList.add("modal-open");

    const modal = el(".modal", scrim);
    const closeBtn = el(".modal-close", scrim);

    function close() {
      scrim.remove();
      document.body.classList.remove("modal-open");
      document.removeEventListener("keydown", onKey);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function onKey(e) {
      if (e.key === "Escape") close();
      if (e.key === "Tab") {
        const focusables = els("button, [href], input", modal).filter((n) => !n.disabled);
        if (focusables.length === 0) return;
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    }

    scrim.addEventListener("click", (e) => { if (e.target === scrim) close(); });
    closeBtn.addEventListener("click", close);
    document.addEventListener("keydown", onKey);
    closeBtn.focus();
  }

  /* ---- modal ---- */

  let lastFocus = null;

  function openModal(item, type) {
    lastFocus = document.activeElement;

    const buffs = item.stats.filter((s) => s.kind === "buff" && s.key !== "SCALE");
    const debuffs = item.stats.filter((s) => s.kind === "debuff" && s.key !== "SCALE");
    const sizeStat = item.stats.find((s) => s.key === "SCALE");

    const buffList = buffs.length
      ? buffs.map((s) => `
        <div class="stat-row">
          <span class="stat-label">${s.label}</span>
          <span class="stat-val">${statFriendly(s)}</span>
        </div>`).join("")
      : `<p class="empty-note">No blessings recorded.</p>`;

    const debuffList = debuffs.length
      ? debuffs.map((s) => `
        <div class="stat-row">
          <span class="stat-label">${s.label}</span>
          <span class="stat-val">${statFriendly(s)}</span>
        </div>`).join("")
      : `<p class="empty-note">No curses recorded.</p>`;

    const sizeNote = sizeStat
      ? `<p class="empty-note">${sizeStat.label}: ${statFriendly(sizeStat)}.</p>`
      : "";

    const kind = type === "race" ? "Race" : `Class · ${item.group_name || "Group " + item.group}`;

    const scrim = document.createElement("div");
    scrim.className = "modal-scrim";
    scrim.innerHTML = `
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <button class="modal-close" aria-label="Close">✕
          <svg><path d="M6 6 L18 18 M18 6 L6 18"/></svg>
        </button>
        <div class="modal-hero">
          <div class="modal-icon">${iconSVG(item.key, 132)}</div>
          <div>
            <div class="modal-prefix">${item.prefix || ""}</div>
            <h2 class="modal-title" id="modal-title">${item.name}</h2>
            <div class="modal-kind">${kind}</div>
          </div>
        </div>
        <div class="modal-body">
          <p class="modal-flavor">${flavorOf(item.description)}</p>
          <div class="stat-columns">
            <div class="stat-col stat-col--buff">
              <h3>Blessings</h3>
              <div class="stat-list">${buffList}</div>
            </div>
            <div class="stat-col stat-col--debuff">
              <h3>Curses</h3>
              <div class="stat-list">${debuffList}</div>
            </div>
          </div>
          ${sizeNote ? `<div class="stat-columns" style="margin-top:16px"><div class="stat-col"><div class="stat-list">${sizeNote}</div></div></div>` : ""}
        </div>
      </section>`;

    document.body.appendChild(scrim);
    document.body.classList.add("modal-open");

    const modal = el(".modal", scrim);
    const closeBtn = el(".modal-close", scrim);

    function close() {
      scrim.remove();
      document.body.classList.remove("modal-open");
      document.removeEventListener("keydown", onKey);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function onKey(e) {
      if (e.key === "Escape") close();
      if (e.key === "Tab") {
        const focusables = els("button, [href], input", modal).filter((n) => !n.disabled);
        if (focusables.length === 0) return;
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }

    scrim.addEventListener("click", (e) => { if (e.target === scrim) close(); });
    closeBtn.addEventListener("click", close);
    document.addEventListener("keydown", onKey);
    closeBtn.focus();
  }

  /* ---- boot ---- */

  const _cache = {};

  async function loadData() {
    if (_cache[DATA_URL]) return _cache[DATA_URL];
    const res = await fetch(DATA_URL);
    if (!res.ok) throw new Error(`Failed to load ${DATA_URL}: ${res.status}`);
    _cache[DATA_URL] = await res.json();
    return _cache[DATA_URL];
  }

  async function loadJSON(url) {
    if (_cache[url]) return _cache[url];
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`);
    _cache[url] = await res.json();
    return _cache[url];
  }

  async function bootGrid() {
    const page = document.body.dataset.page;
    if (page !== "race" && page !== "class") return;

    const container = el(".grid");
    if (!container) return;

    try {
      const ds = await loadData();
      const items = page === "race" ? ds.races : ds.classes;

      renderGrid(container, items, page, { sections: page === "class" });

      container.addEventListener("click", (e) => {
        const card = e.target.closest(".card");
        if (!card) return;
        const item = items.find((i) => i.key === card.dataset.key);
        if (item) openModal(item, page);
      });

      const searchInput = el(".search input");
      const filtersHost = el("#group-filters") || el(".filters");

      const state = { activeFilter: null };

      if (page === "class" && filtersHost) {
        const groups = [...new Set(items.map((i) => i.group).filter(Boolean))].sort((a, b) => a - b);
        filtersHost.innerHTML = groups.map((g) => {
          const label = (items.find((i) => i.group === g) || {}).group_name || ("Group " + g);
          return `<button class="filter-btn" data-filter="${g}" aria-pressed="false">${label}</button>`;
        }).join("");
      }

      const filterBtns = els(".filter-btn");

      function reapply() {
        applyFilters({ grid: container, items, type: page, searchInput, activeFilter: state.activeFilter });
      }

      if (searchInput) {
        searchInput.addEventListener("input", reapply);
      }

      if (filterBtns.length) {
        for (const btn of filterBtns) {
          btn.addEventListener("click", () => {
            const val = btn.dataset.filter || null;
            state.activeFilter = state.activeFilter === val ? null : val;
            for (const b of filterBtns) b.setAttribute("aria-pressed", "false");
            btn.setAttribute("aria-pressed", String(state.activeFilter === val || (val === null && state.activeFilter === null)));
            if (state.activeFilter === null) {
              for (const b of filterBtns) b.setAttribute("aria-pressed", "false");
            }
            reapply();
          });
        }
      }

      const countEl = el(".page-hero-count");
      if (countEl) countEl.textContent = `${items.length} entries · ${items.filter((i) => i.stats.some((s) => s.kind === "debuff")).length} bear curses`;
      reapply();
    } catch (err) {
      el(".grid").innerHTML =
        `<div class="no-results">Data failed to load. Run <span class="mono">site/scripts/build_data.py</span> to regenerate.</div>`;
      console.error(err);
    }
  }

  async function bootEnchants() {
    if (document.body.dataset.page !== "enchant") return;

    const container = el(".grid");
    if (!container) return;

    try {
      const ds = await loadJSON(ENCHANT_URL);
      const items = ds.enchantments;

      container.innerHTML = items.map((en) => enchantCardFor(en)).join("");

      const searchInput = el(".search input");
      const filtersHost = el("#category-filters") || el(".filters");
      const state = { activeFilter: null };

      const categories = [...new Set(items.map((i) => i.category))];
      if (filtersHost) {
        filtersHost.innerHTML = categories.map((c) =>
          `<button class="filter-btn" data-filter="${c}" aria-pressed="false">${c}</button>`).join("");
      }

      const filterBtns = els(".filter-btn");

      function reapply() {
        applyFilters({
          grid: container, items, type: "enchant", searchInput, activeFilter: state.activeFilter,
          match: ({ item, card, q, activeFilter }) => {
            let ok = true;
            if (q) {
              ok = card.dataset.search.includes(q) ||
                item.incompatible.some((s) => s.toLowerCase().includes(q)) ||
                item.primary.some((s) => s.toLowerCase().includes(q)) ||
                item.secondary.some((s) => s.toLowerCase().includes(q));
            }
            if (ok && activeFilter) ok = item.category === activeFilter;
            return ok;
          },
        });
      }

      container.addEventListener("click", (e) => {
        const card = e.target.closest(".card");
        if (!card) return;
        const en = items.find((i) => i.key === card.dataset.key);
        if (en) openEnchantModal(en);
      });

      if (searchInput) searchInput.addEventListener("input", reapply);

      if (filterBtns.length) {
        for (const btn of filterBtns) {
          btn.addEventListener("click", () => {
            const val = btn.dataset.filter || null;
            state.activeFilter = state.activeFilter === val ? null : val;
            for (const b of filterBtns) b.setAttribute("aria-pressed", "false");
            btn.setAttribute("aria-pressed", String(state.activeFilter === val || (val === null && state.activeFilter === null)));
            if (state.activeFilter === null) for (const b of filterBtns) b.setAttribute("aria-pressed", "false");
            reapply();
          });
        }
      }

      const countEl = el(".page-hero-count");
      if (countEl) countEl.textContent = `${items.length} enchantments`;
      reapply();
    } catch (err) {
      el(".grid").innerHTML =
        `<div class="no-results">Enchant data failed to load. Run <span class="mono">site/scripts/build_enchantments.py</span> to regenerate.</div>`;
      console.error(err);
    }
  }

  async function bootCombos() {
    if (document.body.dataset.page !== "combos") return;

    const chart = el(".combo-chart");
    if (!chart) return;

    try {
      const ds = await loadJSON(COMBO_URL);
      const combos = ds.combos;
      if (!combos || !combos.length) {
        chart.innerHTML = `<div class="no-results">No combos computed. Run <span class="mono">site/scripts/build_combos.py</span>.</div>`;
        return;
      }
      const max = combos[0].score || 1;
      chart.innerHTML = combos.map((c) => {
        const pct = Math.max((c.score / max) * 100, 4);
        return `
          <div class="combo-row">
            <div class="combo-rank">#${c.rank}</div>
            <div class="combo-main">
              <div class="combo-name">
                <span class="combo-race">${c.race_name}</span>
                <span class="combo-classes">${c.class_names.join(" · ")}</span>
              </div>
              <div class="combo-bar"><span class="combo-fill" style="width:${pct}%"></span></div>
            </div>
            <div class="combo-score">${c.score}</div>
          </div>`;
      }).join("");
    } catch (err) {
      chart.innerHTML = `<div class="no-results">Combo data failed to load. Run <span class="mono">site/scripts/build_combos.py</span>.</div>`;
      console.error(err);
    }
  }

  async function bootHome() {
    if (document.body.dataset.page !== "home") return;
    try {
      const ds = await loadData();
      const raceCount = ds.races.length;
      const classCount = ds.classes.length;
      const curseCount = [...ds.races, ...ds.classes].filter((i) =>
        i.stats.some((s) => s.kind === "debuff")).length;
      const elR = el("[data-stat-races]");
      const elC = el("[data-stat-classes]");
      const elX = el("[data-stat-curses]");
      if (elR) elR.textContent = raceCount;
      if (elC) elC.textContent = classCount;
      if (elX) elX.textContent = curseCount;
    } catch (e) {
      console.warn("Home stats unavailable:", e);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => { bootHome(); bootGrid(); bootEnchants(); bootCombos(); });
  } else {
    bootHome();
    bootGrid();
    bootEnchants();
    bootCombos();
  }
})();