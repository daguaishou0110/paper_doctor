# -*- coding: utf-8 -*-
"""Build / refresh the non-tumor epidemiology product line (line=epi)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def dump(name: str, obj) -> None:
    (ROOT / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


EPI_METHODS = [
    {
        "id": "epi01",
        "slug": "exposure-disease-association-rf",
        "line": "epi",
        "name_zh": "暴露–疾病关联 + RF 增量鉴别",
        "name_en": "Exposure–Disease Association with Incremental RF Discrimination",
        "summary": "公开队列中评估城市/环境暴露与疾病结局的关联，并用随机森林量化相对临床基线的增量鉴别价值。",
        "endpoint": "横断面患病 / 鉴别 AUC",
        "data_types": ["survey", "city_environment", "clinical"],
        "analysis_pipeline": [
            "CHARLS（或同类）基线纳排与结局定义",
            "城市级暴露（RUI/PM/NDVI 等）按居住城市匹配",
            "调查加权 logistic：连续 + 分位 + 趋势",
            "限制性立方样条（RCS）看剂量–反应",
            "预设亚组与交互检验",
            "递增随机森林：人口学 → 临床 → +暴露 → +环境 → 全模型，比较验证集 AUC",
        ],
        "reporting_standard": "STROBE（横断面）",
        "quality_band": {
            "jcr": "Q2–Q3",
            "cas": "中科院医学/公卫相关约 3–4 区",
            "note": "横断面+自报结局主推 BMC Musculoskeletal Disorders / BMC Public Health；有纵向发病证据可冲更高公卫刊。",
        },
        "hard_requirements": [
            "明确结局操作化定义与排除流程（STROBE 流程图）",
            "报告调查加权 OR、分位趋势与 RCS 非线性检验",
            "机器学习仅作增量鉴别，不作即时临床预测工具宣传",
            "讨论中限制因果表述，承认城市级暴露与自报偏倚",
        ],
        "reject_risks": [
            "把关联写成因果或干预有效",
            "AUC 增量很小却夸大预测价值",
            "个体拆分导致同城泄漏、无城市外推说明",
            "同模板多结局题目雷同被视作系列灌水",
        ],
        "journal_roles": {
            "primary": ["bmc_msk", "bmc_public_health"],
            "backup": ["clinical_rheumatology", "frontiers_public_health", "ehpm"],
            "stretch": [],
        },
        "sample_figure_set": [
            "STROBE 流程图",
            "暴露空间分布",
            "加权 OR 森林/分位",
            "RCS 曲线",
            "亚组森林图",
            "递增模型 ROC/AUC",
        ],
        "graphical_abstract_prompt": "Nature-style graphical abstract, CHARLS cohort icons, city-level urbanization/environment exposure feeding weighted logistic and random-forest AUC badges, white background, no fake numbers",
    },
    {
        "id": "epi02",
        "slug": "multi-exposure-comparison",
        "line": "epi",
        "name_zh": "多暴露比较（城镇化/污染/绿化）",
        "name_en": "Multi-Exposure Comparison for Disease Odds",
        "summary": "在同一队列中并排比较 RUI、空气污染与绿化等暴露对同一疾病结局的关联与相互解释。",
        "endpoint": "横断面患病",
        "data_types": ["survey", "city_environment"],
        "analysis_pipeline": [
            "统一纳排与结局定义",
            "并行匹配 RUI、PM2.5/NO2、NDVI 等",
            "单暴露与多暴露共同调整模型",
            "比较标准化系数 / AUC 增量",
            "讨论信息重叠与残余解释",
        ],
        "reporting_standard": "STROBE（横断面）",
        "quality_band": {
            "jcr": "Q2–Q3",
            "cas": "中科院公卫/环境相关约 3–4 区",
            "note": "故事偏环境健康时主推 BMC Public Health / EHPM；骨肌结局可回 BMC MSK。",
        },
        "hard_requirements": [
            "预先声明主暴露与敏感性暴露",
            "报告共线性/信息重叠，避免过度因果路径声称",
            "至少一种暴露在调整后仍稳健，或如实报告衰减",
        ],
        "reject_risks": [
            "多暴露模型不稳却强行讲机制路径",
            "未处理城市聚集相关的相关误差",
        ],
        "journal_roles": {
            "primary": ["bmc_public_health", "ehpm"],
            "backup": ["bmc_msk", "frontiers_public_health"],
            "stretch": [],
        },
        "sample_figure_set": [
            "STROBE 流程图",
            "暴露相关矩阵/分布",
            "单 vs 多暴露 OR 对比",
            "增量 AUC 对比",
        ],
        "graphical_abstract_prompt": "Clean schematic: three exposure chips RUI PM2.5 NDVI into disease odds node with comparison bars, white Nature flat vector",
    },
    {
        "id": "epi03",
        "slug": "longitudinal-incident-risk",
        "line": "epi",
        "name_zh": "纵向随访发病风险",
        "name_en": "Longitudinal Incident Risk with City Exposure",
        "summary": "利用 CHARLS 随访波次评估基线暴露与新发疾病风险，报告 HR/IRR 与时间顺序。",
        "endpoint": "新发疾病 / 随访风险",
        "data_types": ["survey_longitudinal", "city_environment"],
        "analysis_pipeline": [
            "排除基线已患，定义随访新发",
            "基线暴露匹配",
            "调查加权 Cox 或离散时间模型",
            "竞争风险/失访敏感性（按数据可得性）",
            "可选时间更新暴露",
        ],
        "reporting_standard": "STROBE（队列）",
        "quality_band": {
            "jcr": "Q1–Q2（有扎实随访时可冲）",
            "cas": "中科院公卫约 2–3 区（视随访质量）",
            "note": "有清晰时间顺序后可冲更高公卫刊；随访定义不稳则降回横断面档。",
        },
        "hard_requirements": [
            "写清随访起止、删失与新发判定",
            "基线排除已患",
            "限制反向因果讨论",
        ],
        "reject_risks": [
            "随访波次定义含糊",
            "把横断面结果包装成发病研究",
        ],
        "journal_roles": {
            "primary": ["bmc_public_health"],
            "backup": ["frontiers_public_health", "ehpm"],
            "stretch": [],
        },
        "sample_figure_set": [
            "队列流程图",
            "随访 KM/累积发病",
            "HR 森林图",
            "亚组交互",
        ],
        "graphical_abstract_prompt": "Longitudinal CHARLS waves timeline, baseline city exposure to incident disease hazard, Nature flat vector, no fake HR numbers",
    },
    {
        "id": "epi04",
        "slug": "effect-modification-subgroups",
        "line": "epi",
        "name_zh": "效应修饰 / 亚组交互",
        "name_en": "Effect Modification and Subgroup Interaction",
        "summary": "以年龄、城乡、教育等为修饰因子，系统报告暴露–疾病关联的异质性与交互。",
        "endpoint": "横断面患病（交互）",
        "data_types": ["survey", "city_environment"],
        "analysis_pipeline": [
            "主效应模型确认关联方向",
            "预设亚组分层 OR",
            "乘积交互项与交互 p 值",
            "探索性结果降调表述",
        ],
        "reporting_standard": "STROBE（横断面）",
        "quality_band": {
            "jcr": "Q2–Q3",
            "cas": "中科院医学/公卫约 3–4 区",
            "note": "适合作为 epi01 的姊妹篇或补充分析主文；单独投稿需交互结果足够清晰。",
        },
        "hard_requirements": [
            "区分预设与探索性亚组",
            "报告交互 p 值与分层 CI",
            "避免多重比较过度解读",
        ],
        "reject_risks": [
            "事后挖亚组当主要发现",
            "样本量不足的交互硬解释机制",
        ],
        "journal_roles": {
            "primary": ["bmc_public_health", "bmc_msk"],
            "backup": ["clinical_rheumatology", "frontiers_public_health"],
            "stretch": [],
        },
        "sample_figure_set": [
            "主效应 OR",
            "分层森林图",
            "交互示意",
        ],
        "graphical_abstract_prompt": "Subgroup forest schematic age education urban-rural modifying exposure-disease link, Nature flat vector",
    },
]

DISEASES = [
    {"id": "skoa", "name_zh": "症状性膝骨关节炎", "name_en": "Symptomatic Knee Osteoarthritis", "category": "骨肌", "specialty_journals": ["bmc_msk", "clinical_rheumatology"], "notes": "CHARLS 自报关节炎+膝痛定义"},
    {"id": "lbp", "name_zh": "慢性腰痛", "name_en": "Chronic Low Back Pain", "category": "骨肌", "specialty_journals": ["bmc_msk"], "notes": "问卷疼痛部位/时长定义"},
    {"id": "fracture", "name_zh": "骨折史", "name_en": "Fracture History", "category": "骨肌", "specialty_journals": ["bmc_msk"], "notes": "自报骨折史"},
    {"id": "htn", "name_zh": "高血压", "name_en": "Hypertension", "category": "心血管", "specialty_journals": ["bmc_public_health"], "notes": "自报诊断或血压阈值"},
    {"id": "dm", "name_zh": "糖尿病", "name_en": "Diabetes", "category": "代谢", "specialty_journals": ["bmc_public_health"], "notes": "自报诊断或血糖/用药"},
    {"id": "depression", "name_zh": "抑郁症状", "name_en": "Depressive Symptoms", "category": "精神心理", "specialty_journals": ["bmc_public_health"], "notes": "CESD 阈值"},
    {"id": "sleep", "name_zh": "睡眠障碍", "name_en": "Sleep Disturbance", "category": "精神心理", "specialty_journals": ["bmc_public_health"], "notes": "睡眠时长/质量条目"},
    {"id": "lung", "name_zh": "慢性肺病", "name_en": "Chronic Lung Disease", "category": "呼吸", "specialty_journals": ["bmc_public_health", "ehpm"], "notes": "自报慢阻肺/慢支等"},
    {"id": "stroke", "name_zh": "卒中史", "name_en": "Stroke History", "category": "心血管", "specialty_journals": ["bmc_public_health"], "notes": "自报卒中"},
    {"id": "heart", "name_zh": "心脏病", "name_en": "Heart Disease", "category": "心血管", "specialty_journals": ["bmc_public_health"], "notes": "自报心脏病"},
    {"id": "obesity", "name_zh": "肥胖", "name_en": "Obesity", "category": "代谢", "specialty_journals": ["bmc_public_health"], "notes": "BMI≥28 或自报"},
    {"id": "memory", "name_zh": "主观记忆下降", "name_en": "Subjective Memory Decline", "category": "认知老化", "specialty_journals": ["bmc_public_health"], "notes": "认知相关自报条目"},
]

EPI_JOURNALS = [
    {
        "id": "bmc_msk",
        "name": "BMC Musculoskeletal Disorders",
        "publisher": "BMC / Springer Nature",
        "scie": True,
        "oa_type": "gold",
        "non_oa_possible": False,
        "apc_usd_range": "约 $2500+（以官网为准）",
        "review_cycle": "常见约 2–5 个月",
        "jcr_category": "Orthopedics / Rheumatology",
        "jcr_quartile": "Q2–Q3",
        "cas_major": "中科院医学大类约 3–4 区",
        "cas_minor": "骨科/风湿相关小类以当年表为准",
        "warning": False,
        "warning_note": "",
        "role_in_factory": "公卫线骨肌主推",
        "line": "epi",
        "specialty_cancers": [],
        "specialty_diseases": ["skoa", "lbp", "fracture"],
        "partition_year": "2025",
        "official_url": "https://bmcmusculoskeletdisord.biomedcentral.com/",
        "examples_2025_2026": [
            {
                "title": "Association and Discriminative Value of the Radical Urbanization Index for Symptomatic Knee Osteoarthritis among Middle-aged and Older Adults in China: A CHARLS-Based Cross-Sectional Study",
                "year": 2026,
                "doi": "",
                "method_id": "epi01",
                "how_done": {
                    "summary": "CHARLS 基线匹配城市 RUI，加权 logistic + RCS + 亚组，再用递增随机森林看 AUC 增量。",
                    "data": "CHARLS 2011 基线 n=8022；城市建成区与夜间灯光构建 RUI；城市年均值环境协变量。",
                    "pipeline": "sKOA=自报关节炎+膝痛 → 加权 logistic（连续/分位）→ RCS → 亚组 → RF：人口学/临床/临床+RUI/环境/全模型比较验证 AUC。",
                    "figures": "流程图、RUI 分布、OR/分位、RCS、亚组森林、递增 ROC。",
                    "factory_match": "本站公卫线 epi01 范文；横断面 STROBE，不做因果承诺。",
                },
            }
        ],
    },
    {
        "id": "bmc_public_health",
        "name": "BMC Public Health",
        "publisher": "BMC / Springer Nature",
        "scie": True,
        "oa_type": "gold",
        "non_oa_possible": False,
        "apc_usd_range": "约 $2500+（以官网为准）",
        "review_cycle": "常见约 2–5 个月",
        "jcr_category": "Public, Environmental & Occupational Health",
        "jcr_quartile": "Q2",
        "cas_major": "中科院医学大类约 3 区（公卫相关）",
        "cas_minor": "",
        "warning": False,
        "warning_note": "",
        "role_in_factory": "公卫线主推（慢病/环境）",
        "line": "epi",
        "specialty_cancers": [],
        "specialty_diseases": ["htn", "dm", "depression", "lung", "sleep"],
        "partition_year": "2025",
        "official_url": "https://bmcpublichealth.biomedcentral.com/",
        "examples_2025_2026": [],
    },
    {
        "id": "clinical_rheumatology",
        "name": "Clinical Rheumatology",
        "publisher": "Springer",
        "scie": True,
        "oa_type": "hybrid",
        "non_oa_possible": True,
        "apc_usd_range": "非 OA 可走订阅通道；OA 另计 APC",
        "review_cycle": "常见约 3–6 个月",
        "jcr_category": "Rheumatology",
        "jcr_quartile": "Q2–Q3",
        "cas_major": "中科院医学大类约 3–4 区",
        "cas_minor": "",
        "warning": False,
        "warning_note": "",
        "role_in_factory": "公卫线骨肌/风湿备投",
        "line": "epi",
        "specialty_cancers": [],
        "specialty_diseases": ["skoa", "lbp"],
        "partition_year": "2025",
        "official_url": "https://link.springer.com/journal/10067",
        "examples_2025_2026": [],
    },
    {
        "id": "frontiers_public_health",
        "name": "Frontiers in Public Health",
        "publisher": "Frontiers",
        "scie": True,
        "oa_type": "gold",
        "non_oa_possible": False,
        "apc_usd_range": "约 $3000+（以官网为准）",
        "review_cycle": "常见约 2–4 个月",
        "jcr_category": "Public, Environmental & Occupational Health",
        "jcr_quartile": "Q2–Q3",
        "cas_major": "中科院医学大类约 3–4 区",
        "cas_minor": "",
        "warning": False,
        "warning_note": "",
        "role_in_factory": "公卫线备投（快审/APC）",
        "line": "epi",
        "specialty_cancers": [],
        "specialty_diseases": [],
        "partition_year": "2025",
        "official_url": "https://www.frontiersin.org/journals/public-health",
        "examples_2025_2026": [],
    },
    {
        "id": "ehpm",
        "name": "Environmental Health and Preventive Medicine",
        "publisher": "BMC / Springer Nature",
        "scie": True,
        "oa_type": "gold",
        "non_oa_possible": False,
        "apc_usd_range": "约 $2500+（以官网为准）",
        "review_cycle": "常见约 2–5 个月",
        "jcr_category": "Public, Environmental & Occupational Health",
        "jcr_quartile": "Q2–Q3",
        "cas_major": "中科院医学大类约 3–4 区",
        "cas_minor": "",
        "warning": False,
        "warning_note": "",
        "role_in_factory": "公卫线环境暴露备投",
        "line": "epi",
        "specialty_cancers": [],
        "specialty_diseases": ["lung", "htn"],
        "partition_year": "2025",
        "official_url": "https://environhealthprevmed.biomedcentral.com/",
        "examples_2025_2026": [],
    },
]


def paper_card(
    *,
    disease: dict,
    method_id: str,
    exposure: str,
    title: str,
    direction: str,
    methods_detail: str,
    analysis_style: str,
    journal_primary: str,
    journals_backup: list,
    status: str,
    feasibility: str,
    risk_tags: list,
    quality_target: str,
    serial: int,
) -> dict:
    did = disease["id"]
    pid = f"{did}_{method_id}"
    writing = next(m["name_zh"] for m in EPI_METHODS if m["id"] == method_id)
    return {
        "id": pid,
        "serial": serial,
        "line": "epi",
        "cancer_id": did,
        "cancer_zh": disease["name_zh"],
        "disease_id": did,
        "method_id": method_id,
        "art_no": method_id,
        "title": title,
        "direction": direction,
        "methods_detail": methods_detail,
        "datasets": ["CHARLS-2011", exposure],
        "disease": disease["name_zh"],
        "analysis_style": analysis_style,
        "writing_style": writing,
        "quality_target": quality_target,
        "journal_primary": journal_primary,
        "journals_backup": journals_backup,
        "journal_stretch": None,
        "feasibility": feasibility,
        "risk_tags": risk_tags,
        "intro": (
            f"公卫线选题：针对{disease['name_zh']}，采用「{writing}」路线。"
            f"核心暴露：{exposure}。公开 CHARLS 队列可复用同一分析管线批量扩展。"
        ),
        "graphical_abstract": f"assets/ga/{pid}.jpg",
        "status": status,
        "exposure": exposure,
        "category": disease["category"],
    }


def build_epi_papers() -> list:
    d = {x["id"]: x for x in DISEASES}
    base_detail = (
        "CHARLS 基线纳排；城市级暴露按居住城市匹配；调查加权 logistic（连续+分位+趋势）；"
        "RCS；预设亚组；递增随机森林比较验证集 AUC；按 STROBE 报告。"
    )
    cards = [
        paper_card(
            disease=d["skoa"],
            method_id="epi01",
            exposure="RUI",
            title="Association and Discriminative Value of the Radical Urbanization Index for Symptomatic Knee Osteoarthritis among Middle-aged and Older Adults in China: A CHARLS-Based Cross-Sectional Study",
            direction="城市激进城镇化指数（RUI）与症状性膝骨关节炎关联，并评估相对临床特征的增量鉴别价值",
            methods_detail=base_detail + " 结局：自报关节炎且膝痛。",
            analysis_style="加权 logistic + RCS + RF 增量 AUC",
            journal_primary="bmc_msk",
            journals_backup=["bmc_public_health", "clinical_rheumatology"],
            status="manuscript",
            feasibility="green",
            risk_tags=["横断面", "自报结局"],
            quality_target="JCR Q2–Q3 / 中科院医学约 3–4 区",
            serial=9001,
        ),
        paper_card(
            disease=d["skoa"],
            method_id="epi02",
            exposure="RUI+PM2.5+NDVI",
            title="Radical Urbanization, Air Pollution, and Greenness in Relation to Symptomatic Knee Osteoarthritis: A Multi-Exposure CHARLS Analysis",
            direction="同一队列中比较 RUI、空气污染与绿化对 sKOA 的关联及信息重叠",
            methods_detail=base_detail + " 多暴露单模型与共同调整模型对比。",
            analysis_style="多暴露 OR 对比 + 增量 AUC",
            journal_primary="bmc_public_health",
            journals_backup=["bmc_msk", "ehpm"],
            status="usable",
            feasibility="green",
            risk_tags=["横断面", "暴露共线性"],
            quality_target="JCR Q2–Q3 / 公卫约 3–4 区",
            serial=9002,
        ),
        paper_card(
            disease=d["lbp"],
            method_id="epi01",
            exposure="RUI",
            title="Radical Urbanization Index and Chronic Low Back Pain among Middle-aged and Older Chinese Adults: Evidence from CHARLS",
            direction="RUI 与慢性腰痛患病关联及临床增量鉴别",
            methods_detail=base_detail + " 结局：慢性腰痛操作化定义。",
            analysis_style="加权 logistic + RCS + RF 增量 AUC",
            journal_primary="bmc_msk",
            journals_backup=["bmc_public_health"],
            status="usable",
            feasibility="green",
            risk_tags=["横断面", "疼痛自报"],
            quality_target="JCR Q2–Q3",
            serial=9003,
        ),
        paper_card(
            disease=d["htn"],
            method_id="epi01",
            exposure="RUI",
            title="City-Level Radical Urbanization and Hypertension among Middle-aged and Older Adults in China: A CHARLS Cross-Sectional Study",
            direction="RUI 与高血压患病关联，量化相对个体危险因素的增量信息",
            methods_detail=base_detail + " 结局：自报高血压或血压阈值。",
            analysis_style="加权 logistic + RCS + RF 增量 AUC",
            journal_primary="bmc_public_health",
            journals_backup=["ehpm", "frontiers_public_health"],
            status="usable",
            feasibility="green",
            risk_tags=["横断面"],
            quality_target="JCR Q2 / 公卫约 3 区",
            serial=9004,
        ),
        paper_card(
            disease=d["dm"],
            method_id="epi01",
            exposure="PM2.5",
            title="Long-term City-Level PM2.5 Exposure and Diabetes Mellitus in Middle-aged and Older Chinese Adults: A CHARLS-Based Analysis",
            direction="城市年均值 PM2.5 与糖尿病患病关联及 RF 增量鉴别",
            methods_detail=base_detail + " 主暴露改为 PM2.5。",
            analysis_style="加权 logistic + RCS + RF 增量 AUC",
            journal_primary="bmc_public_health",
            journals_backup=["ehpm", "frontiers_public_health"],
            status="usable",
            feasibility="green",
            risk_tags=["横断面", "城市级暴露"],
            quality_target="JCR Q2–Q3",
            serial=9005,
        ),
        paper_card(
            disease=d["depression"],
            method_id="epi01",
            exposure="NDVI",
            title="Residential Greenness and Depressive Symptoms in Middle-aged and Older Adults: A CHARLS Cross-Sectional Study",
            direction="城市/区域绿化（NDVI）与抑郁症状关联及增量鉴别",
            methods_detail=base_detail + " 结局：CESD 阈值定义抑郁症状。",
            analysis_style="加权 logistic + RCS + RF 增量 AUC",
            journal_primary="bmc_public_health",
            journals_backup=["frontiers_public_health"],
            status="usable",
            feasibility="green",
            risk_tags=["横断面", "量表阈值敏感"],
            quality_target="JCR Q2–Q3",
            serial=9006,
        ),
        paper_card(
            disease=d["lung"],
            method_id="epi01",
            exposure="RUI",
            title="Radical Urbanization Index and Chronic Lung Disease among Middle-aged and Older Adults in China: Insights from CHARLS",
            direction="RUI 与慢性肺病关联；对照既往 RUI–肺病文献并评估环境协变量解释",
            methods_detail=base_detail + " 结局：自报慢性肺病。",
            analysis_style="加权 logistic + RCS + RF 增量 AUC",
            journal_primary="ehpm",
            journals_backup=["bmc_public_health", "frontiers_public_health"],
            status="usable",
            feasibility="green",
            risk_tags=["横断面", "自报肺病"],
            quality_target="JCR Q2–Q3",
            serial=9007,
        ),
        paper_card(
            disease=d["sleep"],
            method_id="epi01",
            exposure="RUI",
            title="Urban Expansion Quality and Sleep Disturbance in Aging Chinese Adults: A CHARLS Analysis Using the Radical Urbanization Index",
            direction="RUI 与睡眠障碍关联及相对生活方式因素的增量信息",
            methods_detail=base_detail + " 结局：睡眠时长/质量条目定义。",
            analysis_style="加权 logistic + RCS + RF 增量 AUC",
            journal_primary="bmc_public_health",
            journals_backup=["frontiers_public_health"],
            status="usable",
            feasibility="yellow",
            risk_tags=["结局定义需统一", "横断面"],
            quality_target="JCR Q2–Q3",
            serial=9008,
        ),
        paper_card(
            disease=d["heart"],
            method_id="epi02",
            exposure="RUI+PM2.5+NDVI",
            title="Comparing Urbanization Quality, Air Pollution, and Greenness in Relation to Heart Disease: A Multi-Exposure CHARLS Study",
            direction="多暴露并排比较与心脏病患病关联",
            methods_detail=base_detail + " 多暴露比较框架。",
            analysis_style="多暴露 OR 对比",
            journal_primary="bmc_public_health",
            journals_backup=["ehpm"],
            status="usable",
            feasibility="green",
            risk_tags=["横断面"],
            quality_target="JCR Q2–Q3",
            serial=9009,
        ),
        paper_card(
            disease=d["htn"],
            method_id="epi04",
            exposure="RUI",
            title="Age and Urban–Rural Heterogeneity in the Association between Radical Urbanization and Hypertension: A CHARLS Subgroup Analysis",
            direction="年龄与城乡对 RUI–高血压关联的效应修饰",
            methods_detail="在 epi01 主效应基础上做预设亚组与乘积交互；探索性结果降调。",
            analysis_style="分层 OR + 交互检验",
            journal_primary="bmc_public_health",
            journals_backup=["frontiers_public_health"],
            status="usable",
            feasibility="yellow",
            risk_tags=["交互探索性", "多重比较"],
            quality_target="JCR Q2–Q3",
            serial=9010,
        ),
        paper_card(
            disease=d["dm"],
            method_id="epi03",
            exposure="RUI",
            title="Baseline Radical Urbanization Index and Incident Diabetes in CHARLS: A Longitudinal Cohort Analysis",
            direction="基线 RUI 与随访新发糖尿病风险（需排除基线已患）",
            methods_detail="排除基线糖尿病；定义随访新发；加权 Cox/离散时间模型；报告删失与随访定义。",
            analysis_style="纵向发病 HR",
            journal_primary="bmc_public_health",
            journals_backup=["ehpm", "frontiers_public_health"],
            status="usable",
            feasibility="yellow",
            risk_tags=["随访定义需核对", "需多波次清洗"],
            quality_target="JCR Q1–Q2（随访扎实可冲）",
            serial=9011,
        ),
        paper_card(
            disease=d["obesity"],
            method_id="epi01",
            exposure="RUI",
            title="Radical Urbanization and Obesity among Middle-aged and Older Adults in China: Association and Incremental Discrimination in CHARLS",
            direction="RUI 与肥胖关联及相对行为/人口学因素的增量鉴别",
            methods_detail=base_detail + " 结局：BMI 阈值或自报肥胖。",
            analysis_style="加权 logistic + RCS + RF 增量 AUC",
            journal_primary="bmc_public_health",
            journals_backup=["frontiers_public_health"],
            status="usable",
            feasibility="green",
            risk_tags=["横断面"],
            quality_target="JCR Q2–Q3",
            serial=9012,
        ),
    ]
    # Fix duplicate ids for same disease+method: use exposure suffix when collision
    seen = {}
    out = []
    for p in cards:
        key = p["id"]
        if key in seen:
            suffix = (
                p["exposure"]
                .lower()
                .replace("+", "_")
                .replace(".", "")
                .replace(" ", "")[:24]
            )
            p["id"] = f"{key}_{suffix}"
            p["graphical_abstract"] = f"assets/ga/{p['id']}.jpg"
        seen[p["id"]] = True
        out.append(p)
    # Special-case: skoa has both epi01 and epi02 — ids already unique by method
    return out


def main() -> None:
    methods = load("methods.json")
    for m in methods:
        m.setdefault("line", "oncology")
    methods = [m for m in methods if not str(m.get("id", "")).startswith("epi")]
    methods.extend(EPI_METHODS)

    journals = load("journals.json")
    for j in journals:
        j.setdefault("line", "oncology")
    existing = {j["id"] for j in journals}
    for j in EPI_JOURNALS:
        if j["id"] in existing:
            # replace/update epi journal entry
            journals = [x for x in journals if x["id"] != j["id"]]
        journals.append(j)

    papers = load("papers.json")
    for p in papers:
        p.setdefault("line", "oncology")
    papers = [p for p in papers if p.get("line") != "epi"]
    epi_papers = build_epi_papers()
    papers.extend(epi_papers)

    diseases = []
    counts = {}
    for p in epi_papers:
        counts[p["disease_id"]] = counts.get(p["disease_id"], 0) + 1
    for d in DISEASES:
        item = dict(d)
        item["paper_count"] = counts.get(d["id"], 0)
        item["done_count"] = sum(
            1
            for p in epi_papers
            if p["disease_id"] == d["id"] and p["status"] == "manuscript"
        )
        item["usable_count"] = sum(
            1
            for p in epi_papers
            if p["disease_id"] == d["id"] and p["status"] == "usable"
        )
        diseases.append(item)

    examples = load("examples.json")
    examples = [e for e in examples if e.get("method_id", "").startswith("art") or e.get("line") == "oncology" or not str(e.get("method_id", "")).startswith("epi")]
    # drop old epi examples then add
    examples = [e for e in examples if not str(e.get("method_id", "")).startswith("epi")]
    examples.append(
        {
            "title": EPI_JOURNALS[0]["examples_2025_2026"][0]["title"],
            "year": 2026,
            "doi": "",
            "method_id": "epi01",
            "line": "epi",
            "how_done": EPI_JOURNALS[0]["examples_2025_2026"][0]["how_done"],
            "journal_id": "bmc_msk",
            "journal_name": "BMC Musculoskeletal Disorders",
        }
    )

    meta = load("meta.json")
    meta["version"] = "20260729b"
    meta["last_updated"] = "2026-07-29"
    meta["product_scope"] = "双产品线：①公开组学肿瘤预后/分型；②公开队列公卫流行病学（CHARLS 类暴露–疾病）。"
    meta["manuscript_note"] = (
        f"肿瘤线约 {sum(1 for p in papers if p.get('line')!='epi')} 篇选题；"
        f"公卫线已上架 {len(epi_papers)} 篇（成稿 {sum(1 for p in epi_papers if p['status']=='manuscript')} / "
        f"可用 {sum(1 for p in epi_papers if p['status']=='usable')}）。分区投稿前请复核当年口径。"
    )
    meta["lines"] = {
        "oncology": {
            "name_zh": "肿瘤组学",
            "name_en": "Oncology omics",
            "methods_prefix": "art",
            "entity": "cancer",
        },
        "epi": {
            "name_zh": "公卫队列",
            "name_en": "Public-health epidemiology",
            "methods_prefix": "epi",
            "entity": "disease",
        },
    }
    meta["epi_totals"] = {
        "articles": len(epi_papers),
        "ready": sum(1 for p in epi_papers if p["status"] == "manuscript"),
        "usable": sum(1 for p in epi_papers if p["status"] == "usable"),
        "diseases": len(diseases),
        "methods": len(EPI_METHODS),
    }

    dump("methods.json", methods)
    dump("journals.json", journals)
    dump("papers.json", papers)
    dump("diseases.json", diseases)
    dump("examples.json", examples)
    dump("meta.json", meta)
    print(
        f"OK methods={len(methods)} journals={len(journals)} papers={len(papers)} "
        f"epi={len(epi_papers)} diseases={len(diseases)}"
    )


if __name__ == "__main__":
    main()
