# -*- coding: utf-8 -*-
"""Expand epi catalog with CHARLS usable topic cards (no paper-count reduction elsewhere)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

METHODS_META = {
    "epi01": {
        "writing": "暴露–疾病关联 + RF 增量鉴别",
        "analysis": "加权 logistic + RCS + RF 增量 AUC",
        "detail": (
            "CHARLS 基线纳排；城市级暴露按居住城市匹配；调查加权 logistic（连续+分位+趋势）；"
            "RCS；预设亚组；递增随机森林比较验证集 AUC；按 STROBE 报告。"
        ),
        "quality": "JCR Q2–Q3 / 中科院公卫或医学约 3–4 区",
        "primary": "bmc_public_health",
        "backup": ["ehpm", "frontiers_public_health"],
    },
    "epi02": {
        "writing": "多暴露比较（城镇化/污染/绿化）",
        "analysis": "多暴露 OR 对比 + 增量 AUC",
        "detail": (
            "同一纳排与结局定义下并排比较 RUI、PM2.5、NDVI；单暴露与共同调整模型；"
            "报告信息重叠与残余解释；STROBE。"
        ),
        "quality": "JCR Q2–Q3 / 公卫或环境约 3–4 区",
        "primary": "bmc_public_health",
        "backup": ["ehpm", "frontiers_public_health"],
    },
    "epi03": {
        "writing": "纵向随访发病风险",
        "analysis": "纵向发病 HR",
        "detail": (
            "排除基线已患；定义随访新发；基线暴露匹配；加权 Cox/离散时间模型；"
            "报告删失与随访定义；STROBE（队列）。"
        ),
        "quality": "JCR Q1–Q2（随访扎实可冲）",
        "primary": "bmc_public_health",
        "backup": ["ehpm", "frontiers_public_health"],
    },
    "epi04": {
        "writing": "效应修饰 / 亚组交互",
        "analysis": "分层 OR + 交互检验",
        "detail": (
            "主效应确认后做预设亚组与乘积交互；区分预设与探索性结果；STROBE。"
        ),
        "quality": "JCR Q2–Q3",
        "primary": "bmc_public_health",
        "backup": ["frontiers_public_health", "ehpm"],
    },
}

# disease_id -> (zh, category, specialty journals, outcome note)
DISEASES = {
    "skoa": ("症状性膝骨关节炎", "骨肌", ["bmc_msk", "clinical_rheumatology"], "自报关节炎+膝痛"),
    "lbp": ("慢性腰痛", "骨肌", ["bmc_msk"], "慢性腰痛操作化定义"),
    "fracture": ("骨折史", "骨肌", ["bmc_msk"], "自报骨折史"),
    "htn": ("高血压", "心血管", ["bmc_public_health"], "自报诊断或血压阈值"),
    "dm": ("糖尿病", "代谢", ["bmc_public_health"], "自报诊断或血糖/用药"),
    "depression": ("抑郁症状", "精神心理", ["bmc_public_health"], "CESD 阈值"),
    "sleep": ("睡眠障碍", "精神心理", ["bmc_public_health"], "睡眠时长/质量条目"),
    "lung": ("慢性肺病", "呼吸", ["bmc_public_health", "ehpm"], "自报慢性肺病"),
    "stroke": ("卒中史", "心血管", ["bmc_public_health"], "自报卒中"),
    "heart": ("心脏病", "心血管", ["bmc_public_health"], "自报心脏病"),
    "obesity": ("肥胖", "代谢", ["bmc_public_health"], "BMI 阈值或自报"),
    "memory": ("主观记忆下降", "认知老化", ["bmc_public_health"], "认知相关自报条目"),
}

# New cards to add (id, disease, method, exposure, title seed, feasibility, risk_tags, journal override)
NEW_CARDS = [
    ("fracture_epi01", "fracture", "epi01", "RUI", "green", ["横断面", "自报骨折"]),
    ("stroke_epi01", "stroke", "epi01", "RUI", "green", ["横断面", "自报卒中"]),
    ("memory_epi01", "memory", "epi01", "NDVI", "yellow", ["结局定义需统一", "横断面"]),
    ("heart_epi01", "heart", "epi01", "RUI", "green", ["横断面"]),
    ("stroke_epi02", "stroke", "epi02", "RUI+PM2.5+NDVI", "green", ["横断面", "暴露共线性"]),
    ("fracture_epi02", "fracture", "epi02", "RUI+PM2.5+NDVI", "green", ["横断面"]),
    ("obesity_epi02", "obesity", "epi02", "RUI+PM2.5+NDVI", "green", ["横断面"]),
    ("depression_epi02", "depression", "epi02", "RUI+PM2.5+NDVI", "green", ["横断面"]),
    ("lung_epi02", "lung", "epi02", "RUI+PM2.5+NDVI", "green", ["横断面"]),
    ("sleep_epi02", "sleep", "epi02", "RUI+PM2.5+NDVI", "yellow", ["结局定义需统一"]),
    ("lbp_epi02", "lbp", "epi02", "RUI+PM2.5+NDVI", "green", ["横断面", "疼痛自报"]),
    ("htn_epi01_pm25", "htn", "epi01", "PM2.5", "green", ["横断面", "城市级暴露"]),
    ("htn_epi01_ndvi", "htn", "epi01", "NDVI", "green", ["横断面"]),
    ("dm_epi01_rui", "dm", "epi01", "RUI", "green", ["横断面"]),
    ("dm_epi01_ndvi", "dm", "epi01", "NDVI", "green", ["横断面"]),
    ("depression_epi01_rui", "depression", "epi01", "RUI", "green", ["横断面", "量表阈值敏感"]),
    ("sleep_epi01_ndvi", "sleep", "epi01", "NDVI", "yellow", ["结局定义需统一"]),
    ("lung_epi01_pm25", "lung", "epi01", "PM2.5", "green", ["横断面", "城市级暴露"]),
    ("obesity_epi01_pm25", "obesity", "epi01", "PM2.5", "green", ["横断面"]),
    ("skoa_epi01_pm25", "skoa", "epi01", "PM2.5", "green", ["横断面"]),
    ("lbp_epi01_ndvi", "lbp", "epi01", "NDVI", "green", ["横断面"]),
    ("stroke_epi03", "stroke", "epi03", "RUI", "yellow", ["随访定义需核对", "需多波次清洗"]),
    ("htn_epi03", "htn", "epi03", "RUI", "yellow", ["随访定义需核对"]),
    ("heart_epi03", "heart", "epi03", "RUI", "yellow", ["随访定义需核对"]),
    ("lung_epi03", "lung", "epi03", "PM2.5", "yellow", ["随访定义需核对"]),
    ("depression_epi04", "depression", "epi04", "RUI", "yellow", ["交互探索性"]),
    ("skoa_epi04", "skoa", "epi04", "RUI", "yellow", ["交互探索性", "多重比较"]),
    ("memory_epi04", "memory", "epi04", "NDVI", "yellow", ["交互探索性", "结局定义需统一"]),
    ("obesity_epi04", "obesity", "epi04", "RUI", "yellow", ["交互探索性"]),
    ("fracture_epi04", "fracture", "epi04", "RUI", "yellow", ["交互探索性"]),
]


def journal_for(disease_id: str, method: str, meta: dict) -> tuple[str, list]:
    zh, cat, specs, _ = DISEASES[disease_id]
    primary = meta["primary"]
    backup = list(meta["backup"])
    if cat == "骨肌":
        primary = "bmc_msk"
        backup = ["bmc_public_health", "clinical_rheumatology"]
    elif method == "epi02" or "PM" in meta.get("_exp", ""):
        primary = "bmc_public_health"
        if "ehpm" not in backup:
            backup = ["ehpm"] + backup
    if specs:
        # prefer specialty as primary when bone/MSK
        if cat == "骨肌" and specs[0] != primary:
            primary = specs[0]
    return primary, backup


def make_card(pid: str, did: str, method: str, exposure: str, feas: str, risks: list, serial: int) -> dict:
    zh, cat, specs, note = DISEASES[did]
    meta = dict(METHODS_META[method])
    meta["_exp"] = exposure
    primary, backup = journal_for(did, method, meta)
    if did == "skoa" and method == "epi01" and exposure == "PM2.5":
        primary, backup = "bmc_msk", ["bmc_public_health", "ehpm"]
    title = f"CHARLS topic card: {exposure} and {zh} ({method})"  # replaced by unique diversify
    direction = {
        "epi01": f"{exposure} 与{zh}关联，并评估相对个体特征的增量鉴别",
        "epi02": f"同一队列比较 RUI/污染/绿化对{zh}的关联及信息重叠",
        "epi03": f"基线 {exposure} 与随访新发{zh}风险（排除基线已患）",
        "epi04": f"年龄/城乡等对 {exposure}–{zh} 关联的效应修饰",
    }[method]
    return {
        "id": pid,
        "serial": serial,
        "line": "epi",
        "cancer_id": did,
        "cancer_zh": zh,
        "disease_id": did,
        "method_id": method,
        "art_no": method,
        "title": title,
        "direction": direction,
        "methods_detail": meta["detail"] + f" 结局：{note}。主暴露：{exposure}。",
        "datasets": ["CHARLS-2011", exposure] if method != "epi03" else ["CHARLS-2011+", exposure],
        "disease": zh,
        "analysis_style": meta["analysis"],
        "writing_style": meta["writing"],
        "quality_target": meta["quality"],
        "journal_primary": primary,
        "journals_backup": backup,
        "journal_stretch": None,
        "feasibility": feas,
        "risk_tags": risks,
        "intro": (
            f"公卫线选题：针对{zh}，采用「{meta['writing']}」路线。"
            f"核心暴露：{exposure}。公开 CHARLS 队列可复用同一分析管线批量扩展。"
        ),
        "graphical_abstract": f"assets/ga/{pid}.jpg",
        "status": "usable",
        "exposure": exposure,
        "category": cat,
    }


def main() -> None:
    papers = json.loads((ROOT / "papers.json").read_text(encoding="utf-8"))
    existing = {p["id"] for p in papers}
    start_serial = max((p.get("serial") or 0) for p in papers) + 1
    added = []
    for i, (pid, did, method, exposure, feas, risks) in enumerate(NEW_CARDS):
        if pid in existing:
            print("skip existing", pid)
            continue
        card = make_card(pid, did, method, exposure, feas, risks, start_serial + i)
        papers.append(card)
        added.append(pid)
        existing.add(pid)

    # refresh diseases.json
    epi = [p for p in papers if p.get("line") == "epi"]
    diseases = []
    for did, (zh, cat, specs, note) in DISEASES.items():
        subset = [p for p in epi if p.get("disease_id") == did or p.get("cancer_id") == did]
        diseases.append(
            {
                "id": did,
                "name_zh": zh,
                "name_en": {
                    "skoa": "Symptomatic Knee Osteoarthritis",
                    "lbp": "Chronic Low Back Pain",
                    "fracture": "Fracture History",
                    "htn": "Hypertension",
                    "dm": "Diabetes",
                    "depression": "Depressive Symptoms",
                    "sleep": "Sleep Disturbance",
                    "lung": "Chronic Lung Disease",
                    "stroke": "Stroke History",
                    "heart": "Heart Disease",
                    "obesity": "Obesity",
                    "memory": "Subjective Memory Decline",
                }[did],
                "category": cat,
                "specialty_journals": specs,
                "notes": note,
                "paper_count": len(subset),
                "done_count": sum(1 for p in subset if p.get("status") == "manuscript"),
                "usable_count": sum(1 for p in subset if p.get("status") == "usable"),
            }
        )

    (ROOT / "papers.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "diseases.json").write_text(json.dumps(diseases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    meta = json.loads((ROOT / "meta.json").read_text(encoding="utf-8"))
    meta["epi_totals"] = {
        "articles": len(epi),
        "ready": sum(1 for p in epi if p.get("status") == "manuscript"),
        "usable": sum(1 for p in epi if p.get("status") == "usable"),
        "diseases": len(diseases),
        "methods": 4,
    }
    meta["manuscript_note"] = (
        f"肿瘤线约 {sum(1 for p in papers if p.get('line')!='epi')} 篇选题；"
        f"公卫线已上架 {len(epi)} 篇（成稿 {meta['epi_totals']['ready']} / "
        f"可用 {meta['epi_totals']['usable']}）。分区投稿前请复核当年口径。"
    )
    meta["version"] = "20260730a"
    meta["last_updated"] = "2026-07-30"
    (ROOT / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("added", len(added), added)
    print("epi_total", len(epi), "site_total", len(papers))


if __name__ == "__main__":
    main()
