# 字段字典（写法 × 期刊 × 论文）

> 网站数据模型的唯一说明。所有 JSON 必须遵守本字典。分区数据需标注口径年份，正式投稿前复核。

## 1. 写法 `methods.json`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 写法 ID，如 `art01` |
| slug | string | URL 友好名 |
| name_zh | string | 中文短名 |
| name_en | string | 英文全称（写法） |
| summary | string | 一句话说明研究做什么 |
| endpoint | string | 主终点：OS / RFS / DFS / 分型一致性 等 |
| data_types | string[] | 数据类型：clinical / transcriptomic / genomic / immune |
| analysis_pipeline | string[] | 分析步骤要点（短句数组） |
| reporting_standard | string | 如 TRIPOD / TRIPOD+AI |
| quality_band | object | 可匹配分区区间 |
| quality_band.jcr | string | 如 `Q2–Q3` |
| quality_band.cas | string | 如 `中科院医学大类 3–4 区` |
| quality_band.note | string | 冲高/降档条件说明 |
| hard_requirements | string[] | 该写法硬性门槛 |
| reject_risks | string[] | 常见拒稿/降档原因 |
| journal_roles | object | `{ primary, backup, stretch }` → journal id 数组 |
| sample_figure_set | string[] | 标准图套装（KM/ROC/校准/DCA…） |
| graphical_abstract_prompt | string | 文生图默认提示词模板 |

## 2. 期刊 `journals.json`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 期刊 ID，如 `frontiers_oncology` |
| name | string | 刊名 |
| publisher | string | 出版社 |
| scie | boolean | 是否 SCIE |
| oa_type | enum | `gold` / `hybrid` / `subscription` |
| non_oa_possible | boolean | 是否可不付 APC 以非 OA 发表 |
| apc_usd_range | string | 版面费区间，如 `$2000–3500`；未知填 `待核` |
| review_cycle | string | 投稿到首决/接收的典型周期描述 |
| jcr_category | string | JCR 学科 |
| jcr_quartile | string | 如 `Q2` |
| cas_major | string | 中科院大类分区描述 |
| cas_minor | string | 中科院小类分区描述（可空） |
| warning | boolean | 是否在预警名单（口径见 meta） |
| warning_note | string | 预警说明或空串 |
| role_in_factory | string | 在选题库中的角色：主推/备投/冲高/保底/专科 |
| specialty_cancers | string[] | 专科适用癌种（可空） |
| partition_year | string | 分区口径年份，如 `2025` |
| official_url | string | 期刊主页 |
| examples_2025_2026 | array | 范文条目 |
| examples_2025_2026[].title | string | 范文题目 |
| examples_2025_2026[].year | number | 年份 |
| examples_2025_2026[].doi | string | DOI（可空，占位文可无） |
| examples_2025_2026[].method_id | string | 对应写法 id |
| examples_2025_2026[].how_done | object | 这篇怎么做的 |
| examples_2025_2026[].how_done.summary | string | 一句话总括 |
| examples_2025_2026[].how_done.data | string | 数据队列 |
| examples_2025_2026[].how_done.pipeline | string | 分析流水线 |
| examples_2025_2026[].how_done.figures | string | 关键图/表 |
| examples_2025_2026[].how_done.factory_match | string | 与本站写法模板的对应与差异 |

## 6. 范文索引 `examples.json`

由 `inject_examples.py` 从各期刊范文扁平化生成，便于按写法筛选。字段 = 期刊范文条目 + `journal_id` + `journal_name`。

## 3. 论文选题 `papers.json`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 如 `crc_art01` |
| cancer_id | string | 癌种 ID |
| cancer_zh | string | 癌种中文名 |
| method_id | string | 对应写法 |
| art_no | string | art01…art07 |
| title | string | 完整英文章题 |
| direction | string | 研究方向（中文） |
| methods_detail | string | 方法详细说明 |
| datasets | string[] | 数据队列，如 TCGA-COAD/READ、GSE39582 |
| disease | string | 研究病症（通常=癌种） |
| analysis_style | string | 分析方式短标签 |
| writing_style | string | 写法中文名（冗余便于展示） |
| quality_target | string | 可达到的分区质量描述 |
| journal_primary | string | 主推期刊 id |
| journals_backup | string[] | 备投期刊 id |
| journal_stretch | string \| null | 冲高期刊 id |
| feasibility | enum | `green` / `yellow` / `red` |
| risk_tags | string[] | 如 `弱外部验证`、`题目待修` |
| intro | string | 列表/详情用简介（2–4 句） |
| graphical_abstract | string | 图片路径或 prompt；原型阶段可用 SVG 占位 |
| status | enum | `draft` / `data_ready` / `analysis` / `manuscript` / `submitted` |

## 4. 癌种 `cancers.json`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 如 `crc` |
| name_zh | string | 结直肠癌 |
| name_en | string | Colorectal Cancer |
| paper_count | number | 选题篇数 |
| specialty_journals | string[] | 专科备投刊 id |
| notes | string | 备注 |

## 5. 元信息 `meta.json`

| 字段 | 类型 | 说明 |
|------|------|------|
| partition_disclaimer | string | 分区免责声明 |
| warning_source | string | 预警名单口径说明 |
| last_updated | string | ISO 日期 |
| version | string | 数据版本 |
