# -*- coding: utf-8 -*-
"""Expand website papers.json / cancers.json from 进度总览.json (not only the original 63)."""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEB = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent
PROGRESS = ROOT / "进度总览.json"

# Chinese folder name → website cancer_id
CANCER_MAP = {
    "结直肠癌": ("crc", "Colorectal Cancer", "TCGA-COAD/READ", ["bmc_gastro"]),
    "结肠腺癌": ("coad", "Colon Adenocarcinoma", "TCGA-COAD", ["bmc_gastro"]),
    "直肠腺癌": ("read", "Rectum Adenocarcinoma", "TCGA-READ", ["bmc_gastro"]),
    "乳腺癌": ("brca", "Breast Invasive Carcinoma", "TCGA-BRCA", ["breast_cancer_tokyo"]),
    "胃腺癌": ("stad", "Stomach Adenocarcinoma", "TCGA-STAD", ["bmc_gastro"]),
    "肺腺癌": ("luad", "Lung Adenocarcinoma", "TCGA-LUAD", ["thoracic_cancer"]),
    "肺鳞癌": ("lusc", "Lung Squamous Cell Carcinoma", "TCGA-LUSC", ["thoracic_cancer"]),
    "肝细胞癌": ("lihc", "Hepatocellular Carcinoma", "TCGA-LIHC", ["hepatology_research"]),
    "胰腺腺癌": ("paad", "Pancreatic Adenocarcinoma", "TCGA-PAAD", ["bmc_gastro"]),
    "头颈鳞癌": ("hnsc", "Head and Neck Squamous Cell Carcinoma", "TCGA-HNSC", ["head_neck"]),
    "肾透明细胞癌": ("kirc", "Clear Cell Renal Cell Carcinoma", "TCGA-KIRC", ["bmc_urology"]),
    "膀胱尿路上皮癌": ("blca", "Bladder Urothelial Carcinoma", "TCGA-BLCA", ["bmc_urology"]),
    "食管癌": ("esca", "Esophageal Carcinoma", "TCGA-ESCA", ["bmc_gastro"]),
    "卵巢浆液性癌": ("ov", "Ovarian Serous Cystadenocarcinoma", "TCGA-OV", []),
    "宫颈癌": ("cesc", "Cervical Squamous Cell Carcinoma", "TCGA-CESC", []),
    "子宫内膜癌": ("ucec", "Uterine Corpus Endometrial Carcinoma", "TCGA-UCEC", []),
    "前列腺癌": ("prad", "Prostate Adenocarcinoma", "TCGA-PRAD", ["bmc_urology"]),
    "皮肤黑色素瘤": ("skcm", "Skin Cutaneous Melanoma", "TCGA-SKCM", []),
    "胶质母细胞瘤": ("gbm", "Glioblastoma Multiforme", "TCGA-GBM", []),
    "甲状腺癌": ("thca", "Thyroid Carcinoma", "TCGA-THCA", []),
    "肾乳头状细胞癌": ("kirp", "Kidney Renal Papillary Cell Carcinoma", "TCGA-KIRP", ["bmc_urology"]),
    "肾嫌色细胞癌": ("kich", "Kidney Chromophobe", "TCGA-KICH", ["bmc_urology"]),
    "胆管癌": ("chol", "Cholangiocarcinoma", "TCGA-CHOL", ["bmc_gastro"]),
    "间皮瘤": ("meso", "Mesothelioma", "TCGA-MESO", ["thoracic_cancer"]),
    "低级别胶质瘤": ("lgg", "Brain Lower Grade Glioma", "TCGA-LGG", []),
    "睾丸生殖细胞瘤": ("tgct", "Testicular Germ Cell Tumors", "TCGA-TGCT", ["bmc_urology"]),
    "葡萄膜黑色素瘤": ("uvm", "Uveal Melanoma", "TCGA-UVM", []),
    "子宫癌肉瘤": ("ucs", "Uterine Carcinosarcoma", "TCGA-UCS", []),
    # additional solid / soft-tissue cohorts on the decision desk
    "骨肉瘤": ("os", "Osteosarcoma", "TARGET-OS", []),
    "软组织肉瘤": ("sarc", "Soft Tissue Sarcoma", "TCGA-SARC", []),
    "神经母细胞瘤": ("nbl", "Neuroblastoma", "TARGET-NBL", []),
    "嗜铬细胞瘤": ("pcpg", "Pheochromocytoma and Paraganglioma", "TCGA-PCPG", []),
    "肾上腺皮质癌": ("acc", "Adrenocortical Carcinoma", "TCGA-ACC", []),
    "胸腺瘤": ("thym", "Thymoma", "TCGA-THYM", []),
    "横纹肌肉瘤": ("rms", "Rhabdomyosarcoma", "TARGET-RMS", []),
    "横纹肌样瘤": ("rt", "Rhabdoid Tumor", "TARGET-RT", []),
    "肾母细胞瘤": ("wt", "Wilms Tumor", "TARGET-WT", []),
    "肾透明细胞肉瘤": ("ccsk", "Clear Cell Sarcoma of the Kidney", "TARGET-CCSK", []),
    "转移性乳腺癌": ("mbrca", "Metastatic Breast Cancer", "METABRIC/GEO", ["breast_cancer_tokyo"]),
    "转移性前列腺癌": ("mprad", "Metastatic Prostate Cancer", "GEO/SU2C", ["bmc_urology"]),
    "弥漫大B细胞淋巴瘤": ("dlbc", "Diffuse Large B-Cell Lymphoma", "TCGA-DLBC", []),
    "急性髓系白血病": ("aml", "Acute Myeloid Leukemia", "TCGA-LAML", []),
}

METHOD_META = {
    "art01": {
        "analysis_style": "临床+转录组 OS 建模与外部验证",
        "quality_target": "JCR Q2 / 中科院医学约 3 区（强结果可冲 2 区）",
        "journal_primary": "frontiers_oncology",
        "journals_backup": ["bmc_cancer", "cancers", "scientific_reports"],
        "journal_stretch": "jtm",
        "feasibility": "green",
        "writing_style": "公开组学标志物挖掘与预后生存建模",
        "direction": "临床特征联合转录组构建总生存（OS）预后模型，并做跨队列/外部验证",
    },
    "art02": {
        "analysis_style": "临床+突变/TMB/MMR OS 建模",
        "quality_target": "JCR Q2 / 中科院医学约 3 区",
        "journal_primary": "frontiers_oncology",
        "journals_backup": ["bmc_cancer", "cancers", "scientific_reports"],
        "journal_stretch": None,
        "feasibility": "green",
        "writing_style": "公开组学标志物挖掘与预后生存建模",
        "direction": "临床特征联合体细胞突变、TMB 与 MMR 状态构建 OS 预后模型",
    },
    "art03": {
        "analysis_style": "临床+转录组 RFS/DFS 建模",
        "quality_target": "JCR Q2 / 中科院医学约 3 区",
        "journal_primary": "bmc_cancer",
        "journals_backup": ["frontiers_oncology", "cancers", "scientific_reports"],
        "journal_stretch": None,
        "feasibility": "yellow",
        "writing_style": "公开组学标志物挖掘与预后生存建模",
        "direction": "临床特征联合转录组预测无复发生存/无病生存（RFS/DFS）",
    },
    "art04": {
        "analysis_style": "风险评分×辅助化疗交互分析",
        "quality_target": "JCR Q2–Q3 / 中科院医学约 3–4 区",
        "journal_primary": "bmc_cancer",
        "journals_backup": ["frontiers_oncology", "scientific_reports", "peerj"],
        "journal_stretch": None,
        "feasibility": "yellow",
        "writing_style": "预后生存建模（风险评分与辅助化疗治疗交互分析）",
        "direction": "转录组风险评分与辅助化疗获益的治疗交互分析（II/III期）",
    },
    "art05": {
        "analysis_style": "分子分型跨平台一致性验证",
        "quality_target": "JCR Q1（综合）/ 中科院约 3 区",
        "journal_primary": "scientific_reports",
        "journals_backup": ["peerj", "cancers"],
        "journal_stretch": None,
        "feasibility": "green",
        "writing_style": "公开组学跨平台分子分型验证",
        "direction": "分子共识分型在 RNA-seq 与芯片平台间的跨平台一致性验证及预后分层",
    },
    "art06": {
        "analysis_style": "临床+免疫+TMB/MMR 整合 OS",
        "quality_target": "JCR Q2 / 中科院医学约 3 区（强结果可冲 2 区）",
        "journal_primary": "frontiers_oncology",
        "journals_backup": ["bmc_cancer", "scientific_reports"],
        "journal_stretch": "jtm",
        "feasibility": "green",
        "writing_style": "公开组学标志物挖掘与预后生存建模",
        "direction": "临床特征联合免疫相关签名、TMB 与 MMR 状态的整合 OS 预后模型",
    },
    "art07": {
        "analysis_style": "II/III 期亚组 RFS 建模",
        "quality_target": "JCR Q2–Q3 / 中科院医学约 3–4 区",
        "journal_primary": "bmc_cancer",
        "journals_backup": ["scientific_reports", "peerj"],
        "journal_stretch": None,
        "feasibility": "yellow",
        "writing_style": "预后生存建模（分期亚组RFS）",
        "direction": "II/III期亚组中的临床+转录组无复发生存建模与亚组分层",
    },
    "art08": {
        "analysis_style": "多模型机器学习生存建模（Cox/RSF/GBSA）与可解释性",
        "quality_target": "JCR Q2 / 中科院医学约 3 区（强外部验证可冲 2 区）",
        "journal_primary": "frontiers_oncology",
        "journals_backup": ["bmc_cancer", "cancers", "scientific_reports", "peerj"],
        "journal_stretch": "jtm",
        "feasibility": "green",
        "writing_style": "多模型机器学习预后建模（临床+转录组OS）",
        "direction": "临床联合转录组，比较多种机器学习生存模型并报告可解释性与外部验证",
    },
}

STATUS_MAP = {
    "完稿": "manuscript",
    "可用": "usable",
    "失败稿": "failed",
    "分析完成": "analyzed",
    "代码就绪": "code_ready",
    "待开发": "todo",
}


def article_method_id(dirname: str) -> str | None:
    m = re.match(r"article(\d+)_", dirname)
    if not m:
        return None
    return f"art{int(m.group(1)):02d}"


def extract_title(tex: Path) -> str | None:
    if not tex.exists():
        return None
    text = tex.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"\\title\{(.+?)\}", text, re.DOTALL)
    if not m:
        return None
    title = m.group(1)
    title = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", title)
    title = re.sub(r"[{}\\]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title or None


def extract_datasets(article: Path, title: str) -> list[str]:
    ds: list[str] = []
    text = title
    summary = article / "data" / "processed" / "analysis_summary.json"
    if summary.exists():
        try:
            text += " " + summary.read_text(encoding="utf-8", errors="ignore")[:4000]
        except Exception:
            pass
    for m in re.findall(r"TCGA-[A-Z0-9/]+", text):
        if m not in ds:
            ds.append(m)
    for m in re.findall(r"GSE\d+", text):
        if m not in ds:
            ds.append(m)
    return ds


def main() -> None:
    rows = json.loads(PROGRESS.read_text(encoding="utf-8"))
    factory = Counter(r["overall"] for r in rows)

    # Keep existing core papers as template for specialty backups when present
    old_papers = []
    old_path = DATA / "papers.json"
    if old_path.exists():
        old_papers = json.loads(old_path.read_text(encoding="utf-8"))
    old_by_id = {p["id"]: p for p in old_papers}

    papers = []
    cancers_used: dict[str, dict] = {}
    serial = 0

    for r in rows:
        cancer_zh = r["cancer"]
        if cancer_zh not in CANCER_MAP:
            continue  # skip special cohorts (ALCHEMIST/CPTAC/HIV…) on the decision desk
        cid, en, tcga, specialty = CANCER_MAP[cancer_zh]
        mid = article_method_id(r.get("dir") or "")
        if not mid or mid not in METHOD_META:
            continue
        overall = r["overall"]
        # Shelf shows completed + usable manuscripts; hide failed/todo noise
        if overall not in {"完稿", "可用"}:
            continue

        article = ROOT / cancer_zh / r["dir"]
        tex_title = extract_title(article / "manuscript" / "manuscript.tex")
        base = old_by_id.get(f"{cid}_{mid}", {})
        # Prefer previously curated unique English titles over homogenizing tex defaults
        title = base.get("title") or tex_title
        if not title:
            title = f"{en}: {METHOD_META[mid]['analysis_style']}"

        meta = METHOD_META[mid]
        pid = f"{cid}_{mid}"
        # Prefer hand-curated journal fields from original 63 when available
        backups = list(base.get("journals_backup") or meta["journals_backup"])
        for s in specialty:
            if s not in backups:
                backups.append(s)

        status = STATUS_MAP.get(overall, "data_ready")
        risk_tags = list(base.get("risk_tags") or [])
        if mid in {"art03", "art04", "art07"} and "依赖复发/化疗信息完整性" not in risk_tags:
            risk_tags.append("依赖复发/化疗信息完整性")
        if mid == "art04" and "可能阴性结果需降档" not in risk_tags:
            risk_tags.append("可能阴性结果需降档")
        if overall == "可用":
            if "缺主图或数据不完整，投稿前复核" not in risk_tags:
                risk_tags.append("缺主图或数据不完整，投稿前复核")
            # honest annotation from factory upgrade
            summary = article / "data" / "processed" / "analysis_summary.json"
            if summary.exists():
                try:
                    sj = json.loads(summary.read_text(encoding="utf-8"))
                    for t in sj.get("risk_tags") or []:
                        if t not in risk_tags:
                            risk_tags.append(t)
                except Exception:
                    pass
        else:
            risk_tags = [t for t in risk_tags if "缺主图" not in t]

        serial += 1
        intro = (
            f"本研究针对{cancer_zh}，采用「{meta['writing_style']}」路线。"
            f"核心方向：{base.get('direction') or meta['direction']}。"
        )
        paper = {
            "id": pid,
            "serial": serial,
            "line": "oncology",
            "cancer_id": cid,
            "cancer_zh": cancer_zh,
            "method_id": mid,
            "art_no": mid,
            "title": title,
            "direction": base.get("direction") or meta["direction"],
            "methods_detail": base.get("methods_detail")
            or f"基于标准分析模板在 {cancer_zh} 队列完成分析与稿件；细节见 manuscript.tex / analysis_summary.json。",
            "datasets": base.get("datasets") or extract_datasets(article, title) or [tcga],
            "disease": cancer_zh,
            "analysis_style": meta["analysis_style"],
            "writing_style": meta["writing_style"],
            "quality_target": meta["quality_target"],
            "journal_primary": base.get("journal_primary") or meta["journal_primary"],
            "journals_backup": backups,
            "journal_stretch": base.get("journal_stretch", meta["journal_stretch"]),
            "feasibility": "green" if overall == "完稿" else "yellow",
            "risk_tags": risk_tags,
            "intro": intro,
            "graphical_abstract": f"assets/ga/{pid}.jpg",
            "status": status,
        }
        if base.get("title_prev"):
            paper["title_prev"] = base["title_prev"]
        papers.append(paper)

        if cid not in cancers_used:
            cancers_used[cid] = {
                "id": cid,
                "name_zh": cancer_zh,
                "name_en": en,
                "tcga": tcga,
                "paper_count": 0,
                "specialty_journals": specialty,
                "notes": "",
                "done_count": 0,
                "usable_count": 0,
            }
        cancers_used[cid]["paper_count"] += 1
        if overall == "完稿":
            cancers_used[cid]["done_count"] += 1
        else:
            cancers_used[cid]["usable_count"] += 1

    # Prefer original core order, then others by done_count
    core_order = ["crc", "brca", "stad", "luad", "lusc", "lihc", "paad", "hnsc", "kirc", "blca", "esca", "ov"]
    rest = sorted(
        (c for c in cancers_used if c not in core_order),
        key=lambda x: (-cancers_used[x]["done_count"], x),
    )
    cancers = []
    for cid in core_order + rest:
        if cid not in cancers_used:
            continue
        c = cancers_used[cid]
        c["notes"] = f"成稿 {c['done_count']} / 收录 {c['paper_count']}"
        cancers.append(c)

    # Deduplicate paper ids (colon vs crc both art01…) — keep first by core preference
    seen = set()
    uniq = []
    for p in papers:
        if p["id"] in seen:
            # rename secondary collision: coad/read already unique; this is for safety
            p["id"] = f"{p['cancer_id']}_{p['method_id']}"
            if p["id"] in seen:
                continue
        seen.add(p["id"])
        uniq.append(p)
    for i, p in enumerate(uniq, 1):
        p["serial"] = i

    # Preserve public-health (epi) shelf cards — oncology expand must not wipe them
    epi_keep = [p for p in old_papers if p.get("line") == "epi"]
    onco_ids = {p["id"] for p in uniq}
    for p in epi_keep:
        if p["id"] not in onco_ids:
            uniq.append(p)
    for i, p in enumerate(uniq, 1):
        p["serial"] = i

    (DATA / "papers.json").write_text(json.dumps(uniq, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "cancers.json").write_text(json.dumps(cancers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    meta_path = DATA / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta["last_updated"] = str(date.today())
    onco = [p for p in uniq if p.get("line") != "epi"]
    epi = [p for p in uniq if p.get("line") == "epi"]
    meta["catalog_totals"] = {
        "articles": len(onco),
        "ready": sum(1 for p in onco if p.get("status") == "manuscript"),
        "usable": sum(1 for p in onco if p.get("status") == "usable"),
    }
    meta["epi_totals"] = {
        "articles": len(epi),
        "ready": sum(1 for p in epi if p.get("status") == "manuscript"),
        "usable": sum(1 for p in epi if p.get("status") == "usable"),
    }
    meta.pop("factory_totals", None)
    meta["manuscript_note"] = (
        f"肿瘤线约 {len(onco)} 篇选题（成稿 {meta['catalog_totals']['ready']} / "
        f"可用 {meta['catalog_totals']['usable']}）；"
        f"公卫线已上架 {len(epi)} 篇（成稿 {meta['epi_totals']['ready']} / "
        f"可用 {meta['epi_totals']['usable']}）。分区投稿前请复核当年口径。"
    )
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "factory": dict(factory),
                "shelf_papers": len(uniq),
                "shelf_oncology": len(onco),
                "shelf_epi": len(epi),
                "shelf_cancers": len(cancers),
                "manuscript_on_shelf": sum(1 for p in uniq if p["status"] == "manuscript"),
                "cancer_ids": [c["id"] for c in cancers],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
