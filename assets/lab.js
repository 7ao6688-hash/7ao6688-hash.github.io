/* Lab tools: flood threshold explorer, InSAR transect, Glasgow greening map. All run on real data
   exported from the case-study repositories (quantised 8-bit PNG grids + lab.json metadata). */
(() => {
  const $ = id => document.getElementById(id);

  // ---------- helpers ----------
  function lut(anchors) {
    const out = new Uint8ClampedArray(256 * 3);
    for (let i = 0; i < 256; i++) {
      const t = (i / 255) * (anchors.length - 1), k = Math.min(anchors.length - 2, Math.floor(t)), f = t - k;
      for (let c = 0; c < 3; c++) out[i * 3 + c] = anchors[k][c] + (anchors[k + 1][c] - anchors[k][c]) * f;
    }
    return out;
  }
  const INFERNO = lut([[0,0,4],[40,11,84],[101,21,110],[159,42,99],[212,72,66],[245,125,21],[250,193,39],[252,255,164]]);
  const DIVERGE = lut([[33,102,172],[103,169,207],[209,229,240],[247,247,247],[253,219,199],[239,138,98],[178,24,43]]);
  const CYCLIC = lut([[226,217,226],[166,187,207],[96,128,190],[67,62,140],[47,20,64],[93,36,78],[166,71,74],[203,135,103],[226,217,226]]);
  const GREENS = lut([[140,81,10],[216,179,101],[246,232,195],[199,234,229],[90,180,172],[1,102,94]]);

  function loadGrid(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        const c = document.createElement("canvas"); c.width = img.width; c.height = img.height;
        const g = c.getContext("2d", { willReadFrequently: true }); g.drawImage(img, 0, 0);
        const rgba = g.getImageData(0, 0, img.width, img.height).data, q = new Uint8Array(img.width * img.height);
        for (let i = 0; i < q.length; i++) q[i] = rgba[i * 4];
        resolve({ q, w: img.width, h: img.height });
      };
      img.onerror = () => reject(new Error("Could not load " + src));
      img.src = src;
    });
  }
  const decode = (meta, q) => q === 0 ? NaN : meta.lo + (q - 1) / 254 * (meta.hi - meta.lo);
  function physical(grid, meta) {
    const v = new Float32Array(grid.q.length);
    for (let i = 0; i < v.length; i++) v[i] = decode(meta, grid.q[i]);
    return v;
  }
  function setupCanvas(canvas, w, h) { canvas.width = w; canvas.height = h; return canvas.getContext("2d"); }
  function pixelAt(canvas, e, w, h) {
    const r = canvas.getBoundingClientRect();
    return [Math.floor((e.clientX - r.left) / r.width * w), Math.floor((e.clientY - r.top) / r.height * h)];
  }
  const fmt = (v, d = 1) => Number.isFinite(v) ? v.toFixed(d) : "–";
  function colourbar(el, table, lo, hi, unit) {
    const stops = [];
    for (let i = 0; i <= 8; i++) { const k = Math.round(i / 8 * 255) * 3; stops.push(`rgb(${table[k]},${table[k + 1]},${table[k + 2]}) ${i * 12.5}%`); }
    el.innerHTML = `<i style="background:linear-gradient(90deg,${stops.join(",")})"></i><span>${lo}</span><span>${unit}</span><span>${hi}</span>`;
  }

  fetch("assets/lab/lab.json").then(r => r.json()).then(meta => {
    floodTool(meta.flood); insarTool(meta.insar); greenTool(meta.glasgow);
  }).catch(err => document.querySelectorAll(".tool-status").forEach(el => { el.hidden = false; el.textContent = err.message; }));

  // ---------- A. flood threshold explorer ----------
  async function floodTool(m) {
    const [gPre, gPost, gB] = await Promise.all([loadGrid("assets/" + m.pre.file), loadGrid("assets/" + m.post.file), loadGrid("assets/" + m.buildings.file)]);
    const { w, h } = gPost, pre = physical(gPre, m.pre), post = physical(gPost, m.post), bld = gB.q;
    const canvas = $("flood-canvas"), ctx = setupCanvas(canvas, w, h), img = ctx.createImageData(w, h);
    const base = new Uint8ClampedArray(w * h);
    for (let i = 0; i < base.length; i++) base[i] = Number.isFinite(post[i]) ? Math.max(0, Math.min(255, (post[i] + 24) / 26 * 255)) : 0;
    const histo = $("flood-hist");
    function render() {
      const thr = +$("flood-thr").value, drop = +$("flood-drop").value;
      let n = 0, b = 0;
      for (let i = 0; i < base.length; i++) {
        const flooded = post[i] < thr && pre[i] >= thr && post[i] - pre[i] <= -drop;
        const g = base[i] * 0.85, k = i * 4;
        if (flooded) { n++; b += bld[i]; img.data[k] = 40; img.data[k + 1] = 150; img.data[k + 2] = 255; }
        else { img.data[k] = g; img.data[k + 1] = g; img.data[k + 2] = g; }
        img.data[k + 3] = 255;
      }
      ctx.putImageData(img, 0, 0);
      $("flood-thr-v").textContent = thr.toFixed(1) + " dB";
      $("flood-drop-v").textContent = drop.toFixed(1) + " dB";
      $("flood-area").textContent = (n * m.pixel_m * m.pixel_m / 1e6).toFixed(1);
      $("flood-bld").textContent = b.toLocaleString("en-GB");
      drawHist(thr);
    }
    const bins = new Array(60).fill(0);
    for (const v of post) if (v > -26 && v < 4) bins[Math.floor((v + 26) / 0.5)]++;
    const maxBin = Math.max(...bins);
    function drawHist(thr) {
      const W = 300, H = 70, x = v => (v + 26) / 30 * W;
      let bars = "";
      bins.forEach((c, i) => {
        const v = -26 + i * 0.5, bh = Math.sqrt(c / maxBin) * (H - 14);
        bars += `<rect x="${x(v).toFixed(1)}" y="${(H - 14 - bh).toFixed(1)}" width="${(W / 60 - 1).toFixed(1)}" height="${bh.toFixed(1)}" fill="${v < thr ? "var(--accent)" : "var(--rule)"}"/>`;
      });
      histo.innerHTML = `${bars}<line x1="${x(thr)}" x2="${x(thr)}" y1="0" y2="${H - 14}" stroke="var(--signal)" stroke-width="2"/>
        <line x1="${x(m.otsu_db)}" x2="${x(m.otsu_db)}" y1="0" y2="${H - 14}" stroke="var(--ink)" stroke-dasharray="3 3"/>
        <text x="0" y="${H - 2}" class="ax">−26 dB</text><text x="${W}" y="${H - 2}" class="ax" text-anchor="end">+4 dB</text>
        <text x="${x(m.otsu_db) + 4}" y="10" class="ax">Otsu</text>`;
    }
    ["flood-thr", "flood-drop"].forEach(id => $(id).addEventListener("input", render));
    $("flood-reset").addEventListener("click", () => { $("flood-thr").value = m.otsu_db; $("flood-drop").value = 3; render(); });
    canvas.addEventListener("pointermove", e => {
      const [cx, cy] = pixelAt(canvas, e, w, h), i = cy * w + cx;
      $("flood-hover").textContent = i >= 0 && i < post.length && Number.isFinite(post[i])
        ? `Before ${fmt(pre[i])} dB → after ${fmt(post[i])} dB (change ${fmt(post[i] - pre[i])} dB)` : "";
    });
    canvas.addEventListener("pointerleave", () => { $("flood-hover").textContent = ""; });
    $("flood-thr").value = m.otsu_db; render();
  }

  // ---------- B. InSAR transect ----------
  async function insarTool(m) {
    const g = await loadGrid("assets/" + m.los.file), { w, h } = g, los = physical(g, m.los);
    const canvas = $("insar-canvas"), ctx = setupCanvas(canvas, w, h), img = ctx.createImageData(w, h);
    const half = m.wavelength_cm / 2;
    let mode = "unwrapped", line = null;
    const ep = [(m.epicentre[0] - m.lon0) / m.deg, (m.lat0 - m.epicentre[1]) / m.deg];
    line = [[ep[0] - 25, ep[1] - 120], [ep[0] + 25, Math.min(h - 2, ep[1] + 150)]];
    function paint() {
      for (let i = 0; i < los.length; i++) {
        const v = los[i], k = i * 4;
        if (!Number.isFinite(v)) { img.data[k] = img.data[k + 1] = img.data[k + 2] = 22; img.data[k + 3] = 255; continue; }
        let idx;
        if (mode === "wrapped") { let p = (v / half) % 1; if (p < 0) p += 1; idx = Math.round(p * 255); }
        else idx = Math.round(Math.max(0, Math.min(1, (v + 15) / 30)) * 255);
        const t = mode === "wrapped" ? CYCLIC : DIVERGE;
        img.data[k] = t[idx * 3]; img.data[k + 1] = t[idx * 3 + 1]; img.data[k + 2] = t[idx * 3 + 2]; img.data[k + 3] = 255;
      }
      ctx.putImageData(img, 0, 0);
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 2.5; ctx.setLineDash([]);
      ctx.beginPath(); ctx.moveTo(...line[0]); ctx.lineTo(...line[1]); ctx.stroke();
      ctx.fillStyle = "#fff";
      for (const [lbl, p] of [["A", line[0]], ["B", line[1]]]) {
        ctx.beginPath(); ctx.arc(p[0], p[1], 5, 0, Math.PI * 2); ctx.fill();
        ctx.font = "bold 13px IBM Plex Mono, monospace"; ctx.fillText(lbl, p[0] + 7, p[1] - 6);
      }
      ctx.strokeStyle = "#111"; ctx.lineWidth = 1.5; ctx.strokeRect(ep[0] - 4, ep[1] - 4, 8, 8);
      $("insar-legend").className = "cbar" + (mode === "wrapped" ? " cyc" : "");
      if (mode === "wrapped") colourbar($("insar-legend"), CYCLIC, "0", half.toFixed(2) + " cm", "one fringe =");
      else colourbar($("insar-legend"), DIVERGE, "−15 cm", "+15 cm", "towards satellite →");
      profile();
    }
    function profile() {
      const [[x0, y0], [x1, y1]] = line, n = Math.max(2, Math.round(Math.hypot(x1 - x0, y1 - y0)));
      const pts = [];
      for (let s = 0; s <= n; s++) {
        const x = Math.round(x0 + (x1 - x0) * s / n), y = Math.round(y0 + (y1 - y0) * s / n);
        pts.push([s * m.km_per_px, los[y * w + x]]);
      }
      const vals = pts.map(p => p[1]).filter(Number.isFinite);
      const W = 520, H = 170, L = 40, R = 10, T = 10, Bm = 26, len = pts[pts.length - 1][0];
      const lo = Math.min(-2, ...vals), hi = Math.max(2, ...vals);
      const X = d => L + d / len * (W - L - R), Y = v => T + (hi - v) / (hi - lo) * (H - T - Bm);
      const line = series => {
        let d = "", pen = false;
        for (const [x, v] of series) { if (!Number.isFinite(v)) { pen = false; continue; } d += (pen ? "L" : "M") + X(x).toFixed(1) + "," + Y(v).toFixed(1); pen = true; }
        return d;
      };
      // Trend: centred moving mean over valid samples only, drawn where enough of the window is measured.
      const k = Math.max(3, Math.round(pts.length / 40));
      const trend = pts.map(([x], i) => {
        let s = 0, c = 0;
        for (let j = Math.max(0, i - k); j <= Math.min(pts.length - 1, i + k); j++) if (Number.isFinite(pts[j][1])) { s += pts[j][1]; c++; }
        return [x, c >= k ? s / c : NaN];
      });
      // Gaps: join the last measured point before each masked stretch to the first one after it.
      const valid = pts.map((p, i) => Number.isFinite(p[1]) ? i : -1).filter(i => i >= 0);
      let gaps = "", widest = null;
      for (let g = 1; g < valid.length; g++) {
        const a = pts[valid[g - 1]], b = pts[valid[g]];
        if (valid[g] - valid[g - 1] < 3) continue;
        gaps += `<line x1="${X(a[0]).toFixed(1)}" y1="${Y(a[1]).toFixed(1)}" x2="${X(b[0]).toFixed(1)}" y2="${Y(b[1]).toFixed(1)}" stroke="var(--muted)" stroke-width="1.3" stroke-dasharray="4 4"/>`;
        if (!widest || X(b[0]) - X(a[0]) > widest.w) widest = { w: X(b[0]) - X(a[0]), x: (X(a[0]) + X(b[0])) / 2, y: Math.min(Y(a[1]), Y(b[1])) - 6 };
      }
      const gapLabel = widest && widest.w > 70 ? `<text x="${widest.x.toFixed(1)}" y="${Math.max(T + 10, widest.y).toFixed(1)}" text-anchor="middle" class="ax">no reliable data</text>` : "";
      const ticks = [lo, 0, hi].map(v => `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" class="grid"/><text x="${L - 6}" y="${Y(v) + 4}" text-anchor="end" class="ax">${v.toFixed(0)}</text>`).join("");
      const key = `<g transform="translate(${W - R - 236},${T})">
        <line x1="0" x2="16" y1="5" y2="5" stroke="var(--accent)" stroke-width="1.6"/><text x="20" y="9" class="ax">measured</text>
        <line x1="80" x2="96" y1="5" y2="5" stroke="var(--accent)" stroke-width="5" stroke-opacity=".3"/><text x="100" y="9" class="ax">trend</text>
        <line x1="138" x2="154" y1="5" y2="5" stroke="var(--muted)" stroke-dasharray="4 3"/><text x="158" y="9" class="ax">no reliable data</text></g>`;
      $("insar-profile").innerHTML = `${ticks}<path d="${line(trend)}" fill="none" stroke="var(--accent)" stroke-opacity=".3" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
        ${gaps}<path d="${line(pts)}" fill="none" stroke="var(--accent)" stroke-width="1.6"/>${gapLabel}${key}
        <text x="${L}" y="${H - 6}" class="ax">A</text><text x="${W - R}" y="${H - 6}" text-anchor="end" class="ax">B · ${len.toFixed(1)} km</text>
        <text x="${(L + W) / 2}" y="${H - 6}" text-anchor="middle" class="ax">LOS displacement (cm)</text>`;
      $("insar-max").textContent = vals.length ? Math.max(...vals).toFixed(1) + " cm" : "–";
      $("insar-range").textContent = vals.length ? (Math.max(...vals) - Math.min(...vals)).toFixed(1) + " cm" : "–";
      $("insar-fr").textContent = vals.length ? ((Math.max(...vals) - Math.min(...vals)) / half).toFixed(1) : "–";
    }
    let dragging = false;
    canvas.addEventListener("pointerdown", e => { e.preventDefault(); canvas.setPointerCapture(e.pointerId); dragging = true; const p = pixelAt(canvas, e, w, h); line = [p, p]; });
    canvas.addEventListener("pointermove", e => {
      const p = pixelAt(canvas, e, w, h);
      if (dragging) { line[1] = p; paint(); }
      const v = los[p[1] * w + p[0]];
      $("insar-hover").textContent = Number.isFinite(v) ? `LOS ${v >= 0 ? "+" : ""}${v.toFixed(1)} cm` : "";
    });
    const end = () => { if (dragging && Math.hypot(line[1][0] - line[0][0], line[1][1] - line[0][1]) < 6) line[1] = [line[0][0] + 1, line[0][1] + 60]; dragging = false; paint(); };
    canvas.addEventListener("pointerup", end); canvas.addEventListener("pointercancel", end);
    canvas.addEventListener("pointerleave", () => { $("insar-hover").textContent = ""; });
    $("insar-wrapped").addEventListener("click", () => { mode = "wrapped"; $("insar-wrapped").setAttribute("aria-pressed", true); $("insar-unwrapped").setAttribute("aria-pressed", false); paint(); });
    $("insar-unwrapped").addEventListener("click", () => { mode = "unwrapped"; $("insar-unwrapped").setAttribute("aria-pressed", true); $("insar-wrapped").setAttribute("aria-pressed", false); paint(); });
    paint();
  }

  // ---------- C. Glasgow greening map ----------
  async function greenTool(m) {
    const [gL, gN, gB] = await Promise.all([loadGrid("assets/" + m.lst.file), loadGrid("assets/" + m.ndvi.file), loadGrid("assets/" + m.builtup)]);
    const { w, h } = gL, lst = physical(gL, m.lst), ndvi = physical(gN, m.ndvi), built = gB.q;
    const canvas = $("green-canvas"), ctx = setupCanvas(canvas, w, h), img = ctx.createImageData(w, h);
    const hot = [];
    for (let i = 0; i < lst.length; i++) if (built[i] && Number.isFinite(lst[i]) && ndvi[i] < 0.35) hot.push(lst[i]);
    hot.sort((a, b) => b - a);
    let view = "lst";
    function render() {
      const share = +$("green-share").value / 100, dn = +$("green-ndvi").value;
      const cut = hot[Math.max(0, Math.min(hot.length - 1, Math.floor(hot.length * share) - 1))];
      let n = 0, sum = 0;
      for (let i = 0; i < lst.length; i++) {
        const v = lst[i], k = i * 4;
        if (!Number.isFinite(v)) { img.data[k] = img.data[k + 1] = img.data[k + 2] = 0; img.data[k + 3] = 0; continue; }
        const pick = built[i] && ndvi[i] < 0.35 && v >= cut;
        if (pick) { n++; sum += v; }
        let r, g, b;
        if (view === "lst") { const t = Math.round(Math.max(0, Math.min(1, (v - 16) / 15)) * 255) * 3; r = INFERNO[t]; g = INFERNO[t + 1]; b = INFERNO[t + 2]; }
        else { const t = Math.round(Math.max(0, Math.min(1, (ndvi[i] + 0.1) / 1.0)) * 255) * 3; r = GREENS[t]; g = GREENS[t + 1]; b = GREENS[t + 2]; }
        if (pick) { r = 70; g = 225; b = 235; }
        img.data[k] = r; img.data[k + 1] = g; img.data[k + 2] = b; img.data[k + 3] = 255;
      }
      ctx.clearRect(0, 0, w, h); ctx.putImageData(img, 0, 0);
      const cool = -m.slope * dn, lo = -m.ci[1] * dn, hi = -m.ci[0] * dn, mean = n ? sum / n : NaN;
      $("green-share-v").textContent = Math.round(share * 100) + "%";
      $("green-ndvi-v").textContent = "+" + dn.toFixed(2);
      $("green-area").textContent = (n * m.pixel_m * m.pixel_m / 1e6).toFixed(1) + " km²";
      $("green-temp").textContent = `${fmt(mean)} → ${fmt(mean - cool)} °C`;
      $("green-cool").textContent = `${cool.toFixed(1)} °C`;
      $("green-ci").textContent = `95% range ${lo.toFixed(1)}–${hi.toFixed(1)} °C`;
      colourbar($("green-legend"), view === "lst" ? INFERNO : GREENS, view === "lst" ? "16 °C" : "−0.1", view === "lst" ? "31 °C" : "0.9",
                view === "lst" ? "surface temperature" : "NDVI");
    }
    ["green-share", "green-ndvi"].forEach(id => $(id).addEventListener("input", render));
    for (const [id, v] of [["green-view-lst", "lst"], ["green-view-ndvi", "ndvi"]]) $(id).addEventListener("click", () => {
      view = v; $("green-view-lst").setAttribute("aria-pressed", v === "lst"); $("green-view-ndvi").setAttribute("aria-pressed", v === "ndvi"); render();
    });
    canvas.addEventListener("pointermove", e => {
      const [cx, cy] = pixelAt(canvas, e, w, h), i = cy * w + cx;
      $("green-hover").textContent = Number.isFinite(lst[i]) ? `${fmt(lst[i])} °C · NDVI ${fmt(ndvi[i], 2)}${built[i] ? " · built-up" : ""}` : "";
    });
    canvas.addEventListener("pointerleave", () => { $("green-hover").textContent = ""; });
    render();
  }
})();
