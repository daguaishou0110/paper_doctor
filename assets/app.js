const state = {
  view: "home",
  selected: null,
  filters: {
    cancer: "",
    method: "",
    nonOaOnly: false,
    scieOnly: true,
    q: "",
  },
  data: {
    meta: null,
    methods: [],
    journals: [],
    cancers: [],
    papers: [],
    examples: [],
  },
};

const $ = (sel) => document.querySelector(sel);

async function loadData() {
  const base = "./data/";
  const [meta, methods, journals, cancers, papers, examples] = await Promise.all([
    fetch(base + "meta.json").then((r) => r.json()),
    fetch(base + "methods.json").then((r) => r.json()),
    fetch(base + "journals.json").then((r) => r.json()),
    fetch(base + "cancers.json").then((r) => r.json()),
    fetch(base + "papers.json").then((r) => r.json()),
    fetch(base + "examples.json").then((r) => r.json()),
  ]);
  state.data = { meta, methods, journals, cancers, papers, examples };
}

function journalById(id) {
  return state.data.journals.find((j) => j.id === id);
}
function methodById(id) {
  return state.data.methods.find((m) => m.id === id);
}
function cancerById(id) {
  return state.data.cancers.find((c) => c.id === id);
}
function paperById(id) {
  return state.data.papers.find((p) => p.id === id);
}

function feasibilityTag(f) {
  if (f === "green") return `<span class="tag ok">可行</span>`;
  if (f === "yellow") return `<span class="tag yellow">慎选</span>`;
  return `<span class="tag danger">风险</span>`;
}

function statusTag(s) {
  if (s === "manuscript") return `<span class="tag ok">成稿</span>`;
  if (s === "usable") return `<span class="tag yellow">可用</span>`;
  if (s === "data_ready") return `<span class="tag muted">数据就绪</span>`;
  return s ? `<span class="tag muted">${escapeXml(s)}</span>` : "";
}

function gaImagePath(paper) {
  return `./assets/ga/${paper.id}.jpg`;
}

function gaSvg(paper) {
  const m = methodById(paper.method_id);
  const label = m ? m.name_zh : paper.method_id;
  const ds = (paper.datasets || []).slice(0, 2).join(" · ") || "公开组学";
  // Prefer Nature-style generated PNG; fall back to SVG placeholder
  return `
  <img class="ga-img" src="${gaImagePath(paper)}" alt="${escapeAttr(paper.cancer_zh)} graphical abstract"
    loading="lazy"
    onerror="this.style.display='none';this.nextElementSibling.style.display='grid';" />
  <div class="ga-fallback" style="display:none;width:100%;height:100%;place-items:center">
  <svg viewBox="0 0 640 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="图形摘要占位">
    <rect width="640" height="360" fill="#f7fbfb"/>
    <rect x="24" y="24" width="592" height="312" rx="16" fill="#ffffff" stroke="#cfe0de"/>
    <text x="48" y="64" font-family="Georgia, serif" font-size="20" fill="#152028">${escapeXml(paper.cancer_zh)}</text>
    <text x="48" y="94" font-family="sans-serif" font-size="14" fill="#0f6e6a">${escapeXml(label)}</text>
    <rect x="48" y="120" width="140" height="64" rx="10" fill="#d8efed"/>
    <text x="68" y="157" font-size="13" fill="#0f6e6a">队列 / 数据</text>
    <path d="M200 152 H250" stroke="#0f6e6a" stroke-width="2"/>
    <rect x="260" y="120" width="140" height="64" rx="10" fill="#e8eef4"/>
    <text x="285" y="157" font-size="13" fill="#4a5b68">建模分析</text>
    <path d="M412 152 H462" stroke="#0f6e6a" stroke-width="2"/>
    <rect x="472" y="120" width="140" height="64" rx="10" fill="#d1fae5"/>
    <text x="500" y="157" font-size="13" fill="#047857">验证评估</text>
    <text x="48" y="230" font-size="12" fill="#4a5b68">${escapeXml(ds)}</text>
    <text x="48" y="260" font-size="12" fill="#4a5b68">${escapeXml(paper.quality_target)}</text>
  </svg>
  </div>`;
}

function escapeXml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function setView(view, selected = null) {
  state.view = view;
  state.selected = selected;
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function navActive(id) {
  const v = state.view;
  if (v === id) return true;
  if (id === "methods" && v === "method") return true;
  if (id === "journals" && v === "journal") return true;
  if (id === "cancers" && v === "paper") return true;
  if (id === "examples" && v === "examples") return true;
  return false;
}

function renderNav() {
  const map = [
    ["home", "首页"],
    ["methods", "写法百科"],
    ["journals", "期刊情报"],
    ["examples", "范文拆解"],
    ["cancers", "癌种选题"],
  ];
  return map
    .map(
      ([id, label]) =>
        `<button type="button" class="${navActive(id) ? "active" : ""}" data-nav="${id}">${label}</button>`
    )
    .join("");
}

function renderHowDone(h) {
  if (!h) return "";
  if (typeof h === "string") return `<p>${h}</p>`;
  return `
    <p><strong>${h.summary || ""}</strong></p>
    <dl class="kv">
      <dt>数据</dt><dd>${h.data || "—"}</dd>
      <dt>怎么做</dt><dd>${h.pipeline || "—"}</dd>
      <dt>图表</dt><dd>${h.figures || "—"}</dd>
      <dt>写法对应</dt><dd>${h.factory_match || "—"}</dd>
    </dl>`;
}

function exampleCard(e) {
  const m = methodById(e.method_id);
  const doiLink = e.doi
    ? `<a href="https://doi.org/${e.doi}" target="_blank" rel="noopener" onclick="event.stopPropagation()">DOI: ${e.doi}</a>`
    : `<span class="tag muted">DOI 待补</span>`;
  return `
  <article class="panel" style="margin:0;box-shadow:none">
    <div class="meta-row">
      <span class="tag">${e.method_id}</span>
      <span class="tag muted">${e.year}</span>
      <span class="tag muted">${e.journal_name || ""}</span>
      ${m ? `<span class="tag ok">${m.name_zh}</span>` : ""}
    </div>
    <h3 style="font-family:var(--font-display);font-size:1.05rem;margin:8px 0">${e.title}</h3>
    <p style="margin:0 0 8px">${doiLink}</p>
    ${renderHowDone(e.how_done)}
    <div class="meta-row" style="margin-top:8px">
      <button class="tag" type="button" data-open-method="${e.method_id}">看写法要求</button>
      ${e.journal_id ? `<button class="tag muted" type="button" data-open-journal="${e.journal_id}">看期刊情报</button>` : ""}
    </div>
  </article>`;
}

function renderHome() {
  const { papers, methods, journals, cancers, meta } = state.data;
  const nonOa = journals.filter((j) => j.non_oa_possible).length;
  const done = papers.filter((p) => p.status === "manuscript").length;
  const usable = papers.filter((p) => p.status === "usable").length;
  const ft = meta.catalog_totals || meta.factory_totals || {};
  const readyN = ft.ready != null ? ft.ready : ft["完稿"] != null ? ft["完稿"] : done;
  const catalogTotal = ft.articles != null ? ft.articles : papers.length;
  return `
  <section class="hero">
    <div>
      <h1>写法选刊 · 病种选题<br/>参考台</h1>
      <p>先看这类写法能匹配几区，再核对期刊是否 SCIE / 非 OA / 预警，最后按癌种挑选可投题目。</p>
    </div>
    <div class="hero-stats">
      <div class="stat"><b>${methods.length}</b><span>写法模板</span></div>
      <div class="stat"><b>${readyN}</b><span>成稿选题</span></div>
      <div class="stat"><b>${done + usable}</b><span>本站收录</span></div>
      <div class="stat"><b>${cancers.length}</b><span>覆盖癌种</span></div>
    </div>
  </section>

  <div class="panel">
    <h2>三步决策</h2>
    <p class="sub">对应核心路径：写法质量 → 期刊约束 → 病种选题；范文拆解帮助对齐「别人怎么发的」。</p>
    <div class="grid">
      <button class="card" type="button" data-nav="methods">
        <h3>1. 写法百科</h3>
        <p>每种写法可冲几区、硬性门槛、拒稿风险、主推/备投/冲高刊。</p>
      </button>
      <button class="card" type="button" data-nav="journals">
        <h3>2. 期刊情报</h3>
        <p>SCIE、OA 类型、非 OA 可能、周期、JCR/中科院、预警。当前可非 OA：${nonOa} 本。</p>
      </button>
      <button class="card" type="button" data-nav="examples">
        <h3>2.5 范文拆解</h3>
        <p>2025–2026（及写法模板）范文：数据、分析流程、图表结构、与本站写法模板对照。</p>
      </button>
      <button class="card" type="button" data-nav="cancers">
        <h3>3. 癌种选题</h3>
        <p>按癌种浏览题目、图形摘要、数据/分析/目标刊。</p>
      </button>
    </div>
  </div>

  <div class="disclaimer">${meta.partition_disclaimer}<br/>${meta.warning_source}${
    meta.manuscript_note ? `<br/>${meta.manuscript_note}` : ""
  }</div>`;
}

function renderMethods() {
  return `
  <div class="panel">
    <h2>写法百科</h2>
    <p class="sub">公开组学预后/分型研究路线。点进卡片看分区要求与期刊角色。</p>
    <div class="grid">
      ${state.data.methods
        .map((m) => {
          const n = state.data.papers.filter((p) => p.method_id === m.id).length;
          return `
        <button class="card" type="button" data-open-method="${m.id}">
          <div class="meta-row">
            <span class="tag">${m.id}</span>
            <span class="tag muted">${m.endpoint}</span>
            <span class="tag muted">${n} 篇选题</span>
          </div>
          <h3>${m.name_zh}</h3>
          <p>${m.summary}</p>
          <div class="meta-row">
            <span class="tag">${m.quality_band.jcr}</span>
            <span class="tag muted">${m.quality_band.cas}</span>
          </div>
        </button>`;
        })
        .join("")}
    </div>
  </div>`;
}

function renderMethodDetail(id) {
  const m = methodById(id);
  if (!m) return `<div class="empty">未找到写法</div>`;
  const relatedEx = state.data.examples.filter((e) => e.method_id === id);
  const journals = (role) =>
    (m.journal_roles[role] || [])
      .map((jid) => {
        const j = journalById(jid);
        return j
          ? `<button class="tag" type="button" data-open-journal="${jid}">${j.name}</button>`
          : "";
      })
      .join(" ");
  return `
  <button class="detail-back" type="button" data-nav="methods">← 返回写法列表</button>
  <div class="panel">
    <div class="meta-row"><span class="tag">${m.id}</span><span class="tag muted">${m.reporting_standard}</span></div>
    <h2 class="detail-title">${m.name_zh}</h2>
    <p class="sub">${m.summary}</p>
    <dl class="kv">
      <dt>可匹配质量</dt><dd>${m.quality_band.jcr} · ${m.quality_band.cas}<br/><span style="color:var(--ink-soft)">${m.quality_band.note}</span></dd>
      <dt>主推期刊</dt><dd class="meta-row">${journals("primary")}</dd>
      <dt>备投期刊</dt><dd class="meta-row">${journals("backup")}</dd>
      <dt>冲高期刊</dt><dd class="meta-row">${journals("stretch") || '<span class="tag muted">无</span>'}</dd>
      <dt>标准图套</dt><dd>${m.sample_figure_set.join(" · ")}</dd>
    </dl>
    <h3>硬性要求</h3>
    <ul class="list-clean">${m.hard_requirements.map((x) => `<li>${x}</li>`).join("")}</ul>
    <h3>常见拒稿/降档</h3>
    <ul class="list-clean">${m.reject_risks.map((x) => `<li>${x}</li>`).join("")}</ul>
    <h3>分析流水线</h3>
    <ul class="list-clean">${m.analysis_pipeline.map((x) => `<li>${x}</li>`).join("")}</ul>
  </div>
  <div class="panel">
    <h2>相关范文（${relatedEx.length}）</h2>
    <p class="sub">看同行怎么做同一类写法；注意「写法对应」里的差异点。</p>
    ${
      relatedEx.length
        ? `<div style="display:grid;gap:12px">${relatedEx.map(exampleCard).join("")}</div>`
        : `<div class="empty">该写法范文待补。可先看「范文拆解」页。</div>`
    }
  </div>`;
}

function renderJournals() {
  const { nonOaOnly, scieOnly, q } = state.filters;
  let list = [...state.data.journals];
  if (scieOnly) list = list.filter((j) => j.scie);
  if (nonOaOnly) list = list.filter((j) => j.non_oa_possible);
  if (q) {
    const qq = q.toLowerCase();
    list = list.filter(
      (j) =>
        j.name.toLowerCase().includes(qq) ||
        j.jcr_category.toLowerCase().includes(qq) ||
        j.role_in_factory.includes(q)
    );
  }
  return `
  <div class="panel">
    <h2>期刊情报</h2>
    <p class="sub">核对 SCIE、OA/非 OA、周期、JCR、中科院、预警；点进期刊可看 2025 前后范文拆解。</p>
    <div class="filters">
      <input type="search" id="journal-q" placeholder="搜索刊名/学科…" value="${escapeAttr(state.filters.q)}" />
      <label class="chip"><input type="checkbox" id="scie-only" ${scieOnly ? "checked" : ""}/> 仅 SCIE</label>
      <label class="chip"><input type="checkbox" id="non-oa-only" ${nonOaOnly ? "checked" : ""}/> 可非 OA</label>
    </div>
    <div class="grid">
      ${
        list.length
          ? list
              .map((j) => {
                return `
        <button class="card" type="button" data-open-journal="${j.id}">
          <div class="meta-row">
            ${j.scie ? '<span class="tag ok">SCIE</span>' : '<span class="tag danger">非 SCIE</span>'}
            <span class="tag muted">${j.oa_type}</span>
            ${j.non_oa_possible ? '<span class="tag ok">可非OA</span>' : '<span class="tag warn">需APC</span>'}
            ${j.warning ? '<span class="tag danger">预警</span>' : ""}
          </div>
          <h3>${j.name}</h3>
          <p>${j.jcr_quartile} · ${j.cas_major}<br/>${j.review_cycle}</p>
          <div class="meta-row"><span class="tag muted">${j.role_in_factory}</span>${
            (j.examples_2025_2026 || []).length
              ? `<span class="tag ok">${j.examples_2025_2026.length} 范文</span>`
              : ""
          }</div>
        </button>`;
              })
              .join("")
          : `<div class="empty">没有符合筛选的期刊</div>`
      }
    </div>
  </div>`;
}

function renderJournalDetail(id) {
  const j = journalById(id);
  if (!j) return `<div class="empty">未找到期刊</div>`;
  const related = state.data.papers.filter(
    (p) =>
      p.journal_primary === id ||
      (p.journals_backup || []).includes(id) ||
      p.journal_stretch === id
  );
  const exs = (j.examples_2025_2026 || []).map((e) => ({
    ...e,
    journal_id: j.id,
    journal_name: j.name,
  }));
  return `
  <button class="detail-back" type="button" data-nav="journals">← 返回期刊列表</button>
  <div class="panel">
    <div class="meta-row">
      ${j.scie ? '<span class="tag ok">SCIE</span>' : ""}
      <span class="tag muted">${j.oa_type}</span>
      ${j.non_oa_possible ? '<span class="tag ok">可非OA</span>' : '<span class="tag warn">Gold OA / 需 APC</span>'}
      ${j.warning ? '<span class="tag danger">预警</span>' : '<span class="tag ok">未标预警</span>'}
      ${exs.length ? `<span class="tag ok">${exs.length} 篇范文</span>` : ""}
    </div>
    <h2 class="detail-title">${j.name}</h2>
    <p class="sub">${j.publisher} · 分区口径 ${j.partition_year}</p>
    <dl class="kv">
      <dt>JCR</dt><dd>${j.jcr_category} · ${j.jcr_quartile}</dd>
      <dt>中科院</dt><dd>${j.cas_major}${j.cas_minor ? "；" + j.cas_minor : ""}</dd>
      <dt>投稿周期</dt><dd>${j.review_cycle}</dd>
      <dt>版面费</dt><dd>${j.apc_usd_range}</dd>
      <dt>选刊角色</dt><dd>${j.role_in_factory}</dd>
      <dt>官网</dt><dd><a href="${j.official_url}" target="_blank" rel="noopener">${j.official_url}</a></dd>
      <dt>预警说明</dt><dd>${j.warning_note || "无"}</dd>
    </dl>
  </div>
  <div class="panel">
    <h2>范文拆解（${exs.length}）</h2>
    <p class="sub">这篇怎么做的：数据 → 分析流程 → 图表 → 与本站写法模板对照。</p>
    ${
      exs.length
        ? `<div style="display:grid;gap:12px">${exs.map(exampleCard).join("")}</div>`
        : `<div class="empty">该刊范文待补。</div>`
    }
  </div>
  <div class="panel">
    <h2>关联选题（${related.length}）</h2>
    <div class="grid">
      ${related
        .slice(0, 12)
        .map(
          (p) => `
        <button class="card" type="button" data-open-paper="${p.id}">
          <div class="meta-row">${feasibilityTag(p.feasibility)}<span class="tag muted">${p.cancer_zh}</span><span class="tag">${p.method_id}</span></div>
          <h3 style="font-size:.95rem">${p.title}</h3>
        </button>`
        )
        .join("")}
    </div>
  </div>`;
}

function renderExamples() {
  const method = state.filters.method;
  let list = [...state.data.examples];
  if (method) list = list.filter((e) => e.method_id === method);
  return `
  <div class="panel">
    <h2>范文拆解</h2>
    <p class="sub">2025–2026 为主（个别写法模板参考略早）。每篇拆成：数据 / 怎么做 / 图表 / 写法对应。</p>
    <div class="filters">
      <select id="filter-method-ex">
        <option value="">全部写法</option>
        ${state.data.methods
          .map(
            (m) =>
              `<option value="${m.id}" ${method === m.id ? "selected" : ""}>${m.id} · ${m.name_zh}</option>`
          )
          .join("")}
      </select>
      <span class="tag muted">共 ${list.length} 篇</span>
    </div>
    ${
      list.length
        ? `<div style="display:grid;gap:12px">${list.map(exampleCard).join("")}</div>`
        : `<div class="empty">没有符合筛选的范文</div>`
    }
  </div>`;
}

function renderCancers() {
  const { cancer, method, q } = state.filters;
  let list = [...state.data.papers];
  if (cancer) list = list.filter((p) => p.cancer_id === cancer);
  if (method) list = list.filter((p) => p.method_id === method);
  if (q) {
    const qq = q.toLowerCase();
    list = list.filter(
      (p) =>
        p.title.toLowerCase().includes(qq) ||
        p.direction.includes(q) ||
        p.cancer_zh.includes(q)
    );
  }

  const cancerTabs = state.data.cancers
    .map(
      (c) =>
        `<button type="button" class="chip-btn ${cancer === c.id ? "active" : ""}" data-filter-cancer="${c.id}" style="border:1px solid var(--line);border-radius:999px;padding:8px 12px;background:${
          cancer === c.id ? "var(--accent)" : "#fff"
        };color:${cancer === c.id ? "#fff" : "var(--ink-soft)"};cursor:pointer;font:inherit;font-size:.9rem">${c.name_zh}</button>`
    )
    .join("");

  return `
  <div class="panel">
    <h2>癌种选题</h2>
    <p class="sub">按癌种展开选题：题目、图形摘要、病种/数据/分析/写法/分区质量/目标刊。</p>
    <div class="filters" style="margin-bottom:10px">
      <button type="button" data-filter-cancer="" style="border:1px solid var(--line);border-radius:999px;padding:8px 12px;background:${
        !cancer ? "var(--accent)" : "#fff"
      };color:${!cancer ? "#fff" : "var(--ink-soft)"};cursor:pointer;font:inherit;font-size:.9rem">全部</button>
      ${cancerTabs}
    </div>
    <div class="filters">
      <select id="filter-method">
        <option value="">全部写法</option>
        ${state.data.methods
          .map(
            (m) =>
              `<option value="${m.id}" ${method === m.id ? "selected" : ""}>${m.id} · ${m.name_zh}</option>`
          )
          .join("")}
      </select>
      <input type="search" id="paper-q" placeholder="搜索题目/方向…" value="${escapeAttr(q)}" />
    </div>
    <div class="grid">
      ${
        list.length
          ? list
              .map((p) => {
                const j = journalById(p.journal_primary);
                return `
        <button class="card" type="button" data-open-paper="${p.id}">
          <div class="ga">${gaSvg(p)}</div>
          <div class="meta-row">
            ${statusTag(p.status)}
            ${feasibilityTag(p.feasibility)}
            <span class="tag muted">${p.cancer_zh}</span>
            <span class="tag">${p.method_id}</span>
          </div>
          <h3 style="font-size:.98rem">${p.title}</h3>
          <p>${p.analysis_style}<br/>目标：${j ? j.name : p.journal_primary} · ${p.quality_target}</p>
        </button>`;
              })
              .join("")
          : `<div class="empty">没有符合筛选的论文</div>`
      }
    </div>
  </div>`;
}

function renderPaperDetail(id) {
  const p = paperById(id);
  if (!p) return `<div class="empty">未找到论文</div>`;
  const m = methodById(p.method_id);
  const primary = journalById(p.journal_primary);
  const stretch = p.journal_stretch ? journalById(p.journal_stretch) : null;
  const backups = (p.journals_backup || [])
    .map((jid) => journalById(jid))
    .filter(Boolean);

  return `
  <button class="detail-back" type="button" data-nav="cancers">← 返回癌种选题</button>
  <div class="panel">
    <div class="ga">${gaSvg(p)}</div>
    <div class="meta-row">
      ${statusTag(p.status)}
      ${feasibilityTag(p.feasibility)}
      <span class="tag muted">${p.cancer_zh}</span>
      <span class="tag">${p.method_id}</span>
      ${(p.risk_tags || []).map((t) => `<span class="tag warn">${t}</span>`).join("")}
    </div>
    <h2 class="detail-title">${p.title}</h2>
    <p class="sub">${p.intro}</p>
    <dl class="kv">
      <dt>研究病症</dt><dd>${p.disease}</dd>
      <dt>使用数据</dt><dd>${(p.datasets || []).join(" · ") || "见方法说明 / TCGA+GEO"}</dd>
      <dt>分析方式</dt><dd>${p.analysis_style}</dd>
      <dt>写法</dt><dd><button class="tag" type="button" data-open-method="${p.method_id}">${m ? m.name_zh : p.writing_style}</button></dd>
      <dt>可达质量</dt><dd>${p.quality_target}</dd>
      <dt>主推期刊</dt><dd>${
        primary
          ? `<button class="tag" type="button" data-open-journal="${primary.id}">${primary.name}</button> · ${primary.jcr_quartile} · ${primary.cas_major}${
              primary.non_oa_possible ? ' · <span class="tag ok">可非OA</span>' : ' · <span class="tag warn">OA/APC</span>'
            }`
          : p.journal_primary
      }</dd>
      <dt>备投</dt><dd class="meta-row">${backups
        .map((j) => `<button class="tag muted" type="button" data-open-journal="${j.id}">${j.name}</button>`)
        .join("")}</dd>
      <dt>冲高</dt><dd>${
        stretch
          ? `<button class="tag" type="button" data-open-journal="${stretch.id}">${stretch.name}</button>`
          : '<span class="tag muted">无</span>'
      }</dd>
      <dt>研究方向</dt><dd>${p.direction}</dd>
      <dt>方法要点</dt><dd>${p.methods_detail}</dd>
    </dl>
  </div>`;
}

function escapeAttr(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;");
}

function render() {
  $("#nav").innerHTML = renderNav();
  const root = $("#view");
  if (state.view === "home") root.innerHTML = renderHome();
  else if (state.view === "methods") root.innerHTML = renderMethods();
  else if (state.view === "method") root.innerHTML = renderMethodDetail(state.selected);
  else if (state.view === "journals") root.innerHTML = renderJournals();
  else if (state.view === "journal") root.innerHTML = renderJournalDetail(state.selected);
  else if (state.view === "examples") root.innerHTML = renderExamples();
  else if (state.view === "cancers") root.innerHTML = renderCancers();
  else if (state.view === "paper") root.innerHTML = renderPaperDetail(state.selected);
  bindUi();
}

function bindUi() {
  document.querySelectorAll("[data-nav]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      const target = el.getAttribute("data-nav");
      if (target === "journals" || target === "cancers") {
        /* keep filters */
      } else {
        state.filters.q = "";
      }
      setView(target);
    });
  });
  document.querySelectorAll("[data-open-method]").forEach((el) => {
    el.addEventListener("click", () => setView("method", el.getAttribute("data-open-method")));
  });
  document.querySelectorAll("[data-open-journal]").forEach((el) => {
    el.addEventListener("click", () => setView("journal", el.getAttribute("data-open-journal")));
  });
  document.querySelectorAll("[data-open-paper]").forEach((el) => {
    el.addEventListener("click", () => setView("paper", el.getAttribute("data-open-paper")));
  });
  document.querySelectorAll("[data-filter-cancer]").forEach((el) => {
    el.addEventListener("click", () => {
      state.filters.cancer = el.getAttribute("data-filter-cancer");
      setView("cancers");
    });
  });
  const methodSel = $("#filter-method");
  if (methodSel) {
    methodSel.addEventListener("change", () => {
      state.filters.method = methodSel.value;
      setView("cancers");
    });
  }
  const methodSelEx = $("#filter-method-ex");
  if (methodSelEx) {
    methodSelEx.addEventListener("change", () => {
      state.filters.method = methodSelEx.value;
      setView("examples");
    });
  }
  const paperQ = $("#paper-q");
  if (paperQ) {
    paperQ.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        state.filters.q = paperQ.value.trim();
        setView("cancers");
      }
    });
  }
  const journalQ = $("#journal-q");
  if (journalQ) {
    journalQ.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        state.filters.q = journalQ.value.trim();
        setView("journals");
      }
    });
  }
  const scieOnly = $("#scie-only");
  if (scieOnly) {
    scieOnly.addEventListener("change", () => {
      state.filters.scieOnly = scieOnly.checked;
      setView("journals");
    });
  }
  const nonOa = $("#non-oa-only");
  if (nonOa) {
    nonOa.addEventListener("change", () => {
      state.filters.nonOaOnly = nonOa.checked;
      setView("journals");
    });
  }
}

async function main() {
  try {
    await loadData();
    render();
  } catch (err) {
    $("#view").innerHTML = `<div class="empty">数据加载失败。请用本地静态服务器打开（不要直接双击 file://）。<br/><code>${escapeXml(
      String(err)
    )}</code></div>`;
  }
}

main();
