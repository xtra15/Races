/* ValhallaRaces compendium — shared app logic.
   Handles: data loading + caching, card rendering, live search,
   group filters, and the detail modal with buff/debuff columns. */

(() => {
  "use strict";

  const DATA_URL = "assets/data/data.json";
  let DATASET = null;

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

  function renderGrid(container, items, type) {
    container.innerHTML = items.map((it) => cardFor(it, type)).join("");
  }

  /* ---- search + filter state ---- */

  function applyFilters({ grid, items, type, searchInput, activeFilter }) {
    const q = (searchInput ? searchInput.value : "").trim().toLowerCase();
    const cards = els(".card", grid);

    for (const card of cards) {
      const key = card.dataset.key;
      const item = items.find((i) => i.key === key);
      const matchesSearch =
        !q ||
        card.dataset.search.includes(q) ||
        item.stats.some((s) => s.label.toLowerCase().includes(q));

      const inGroup = !activeFilter || String(item.group) === activeFilter;
      const show = matchesSearch && inGroup;
      card.style.display = show ? "" : "none";
    }

    const visible = cards.filter((c) => c.style.display !== "none").length;
    el(".live-count", grid.closest("[data-page]")) &&
      (el(".live-count", grid.closest("[data-page]")).textContent = `${visible} / ${items.length}`);

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

  async function loadData() {
    if (DATASET) return DATASET;
    const res = await fetch(DATA_URL);
    if (!res.ok) throw new Error(`Failed to load ${DATA_URL}: ${res.status}`);
    DATASET = await res.json();
    return DATASET;
  }

  async function bootPage() {
    const page = document.body.dataset.page;
    if (page !== "race" && page !== "class") return;

    const container = el(".grid");
    if (!container) return;

    try {
      const ds = await loadData();
      const items = page === "race" ? ds.races : ds.classes;

      renderGrid(container, items, page);

      container.addEventListener("click", (e) => {
        const card = e.target.closest(".card");
        if (!card) return;
        const item = items.find((i) => i.key === card.dataset.key);
        if (item) openModal(item, page);
      });

      const searchInput = el(".search input");
      const filtersHost = el("#group-filters") || el(".filters");

      const state = { activeFilter: null };

      // Build group filter buttons dynamically from the dataset
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

      // populate stat chips for bootstrap
      const countEl = el(".page-hero-count");
      if (countEl) countEl.textContent = `${items.length} entries · ${items.filter((i) => i.stats.some((s) => s.kind === "debuff")).length} bear curses`;
      reapply();
    } catch (err) {
      el(".grid").innerHTML =
        `<div class="no-results">Data failed to load. Run <span class="mono">site/scripts/build_data.py</span> to regenerate.</div>`;
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
    document.addEventListener("DOMContentLoaded", () => { bootHome(); bootPage(); });
  } else {
    bootHome();
    bootPage();
  }
})();