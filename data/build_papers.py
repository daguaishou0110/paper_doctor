# -*- coding: utf-8 -*-
"""Generate papers.json from the 63-article markdown master table."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT.parent / "63篇_合并总表_题目方向方法写法期刊分区.md"
OUT = Path(__file__).resolve().parent / "papers.json"

CANCER_MAP = {
    "结直肠癌": "crc",
    "乳腺癌": "brca",
    "胃腺癌": "stad",
    "肺腺癌": "luad",
    "肺鳞癌": "lusc",
    "肝细胞癌": "lihc",
    "胰腺腺癌": "paad",
    "头颈鳞癌": "hnsc",
    "肾透明细胞癌": "kirc",
}

JOURNAL_ALIAS = [
    ("Frontiers in Oncology", "frontiers_oncology"),
    ("BMC Cancer", "bmc_cancer"),
    ("Cancers", "cancers"),
    ("Scientific Reports", "scientific_reports"),
    ("Journal of Translational Medicine", "jtm"),
    ("PeerJ", "peerj"),
    ("Thoracic Cancer", "thoracic_cancer"),
    ("Head & Neck", "head_neck"),
    ("BMC Gastroenterology", "bmc_gastro"),
    ("Hepatology Research", "hepatology_research"),
    ("Breast Cancer (Tokyo)", "breast_cancer_tokyo"),
    ("BMC Urology", "bmc_urology"),
]

# Per-cancer GEO / dataset hints used in titles (fallback extraction from title)
METHOD_META = {
    "art01": {
        "analysis_style": "临床+转录组 OS 建模与外部验证",
        "quality_target": "JCR Q2 / 中科院医学约 3 区（强结果可冲 2 区）",
        "journal_primary": "frontiers_oncology",
        "journals_backup": ["bmc_cancer", "cancers", "scientific_reports"],
        "journal_stretch": "jtm",
        "feasibility": "green",
    },
    "art02": {
        "analysis_style": "临床+突变/TMB/MMR OS 建模",
        "quality_target": "JCR Q2 / 中科院医学约 3 区",
        "journal_primary": "frontiers_oncology",
        "journals_backup": ["bmc_cancer", "cancers", "scientific_reports"],
        "journal_stretch": None,
        "feasibility": "green",
    },
    "art03": {
        "analysis_style": "临床+转录组 RFS/DFS 建模",
        "quality_target": "JCR Q2 / 中科院医学约 3 区",
        "journal_primary": "bmc_cancer",
        "journals_backup": ["frontiers_oncology", "cancers", "scientific_reports"],
        "journal_stretch": None,
        "feasibility": "yellow",
    },
    "art04": {
        "analysis_style": "风险评分×辅助化疗交互分析",
        "quality_target": "JCR Q2–Q3 / 中科院医学约 3–4 区",
        "journal_primary": "bmc_cancer",
        "journals_backup": ["frontiers_oncology", "scientific_reports", "peerj"],
        "journal_stretch": None,
        "feasibility": "yellow",
    },
    "art05": {
        "analysis_style": "分子分型跨平台一致性验证",
        "quality_target": "JCR Q1（综合）/ 中科院约 3 区",
        "journal_primary": "scientific_reports",
        "journals_backup": ["peerj", "cancers"],
        "journal_stretch": None,
        "feasibility": "green",
    },
    "art06": {
        "analysis_style": "临床+免疫+TMB/MMR 整合 OS",
        "quality_target": "JCR Q2 / 中科院医学约 3 区（强结果可冲 2 区）",
        "journal_primary": "frontiers_oncology",
        "journals_backup": ["bmc_cancer", "scientific_reports"],
        "journal_stretch": "jtm",
        "feasibility": "green",
    },
    "art07": {
        "analysis_style": "II/III 期亚组 RFS 建模",
        "quality_target": "JCR Q2–Q3 / 中科院医学约 3–4 区",
        "journal_primary": "bmc_cancer",
        "journals_backup": ["scientific_reports", "peerj"],
        "journal_stretch": None,
        "feasibility": "yellow",
    },
}

SPECIALTY = {
    "crc": "bmc_gastro",
    "brca": "breast_cancer_tokyo",
    "stad": "bmc_gastro",
    "luad": "thoracic_cancer",
    "lusc": "thoracic_cancer",
    "lihc": "hepatology_research",
    "paad": "bmc_gastro",
    "hnsc": "head_neck",
    "kirc": "bmc_urology",
}


def parse_journal_ids(cell: str) -> list[str]:
    if not cell or cell.strip() in {"—", "-", "–"}:
        return []
    found = []
    for name, jid in JOURNAL_ALIAS:
        if name in cell and jid not in found:
            found.append(jid)
    return found


def extract_datasets(title: str, methods: str) -> list[str]:
    text = f"{title} {methods}"
    ds = []
    for m in re.findall(r"TCGA-[A-Z0-9/]+", text):
        if m not in ds:
            ds.append(m)
    for m in re.findall(r"GSE\d+", text):
        if m not in ds:
            ds.append(m)
    return ds


def split_row(line: str) -> list[str]:
    # Markdown table row → cells
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    return parts


def main() -> None:
    lines = MD.read_text(encoding="utf-8").splitlines()
    papers = []
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 10:
            continue
        if cells[0] in {"编号", "------"} or cells[0].startswith("-"):
            continue
        if not cells[0].isdigit():
            continue

        no, cancer_zh, art_no, title, direction, methods_detail, writing, primary_cell, backup_cell, stretch_cell = cells[:10]
        cancer_id = CANCER_MAP[cancer_zh]
        method_id = art_no
        meta = METHOD_META[method_id]

        backups = parse_journal_ids(backup_cell)
        # ensure specialty journal appears in backup if mentioned
        spec = SPECIALTY.get(cancer_id)
        if spec and spec not in backups and (spec in parse_journal_ids(backup_cell) or True):
            # add specialty if present in backup text via alias already; else append if name fragments match
            pass
        # Re-parse and also append specialty id if the Chinese table listed it
        for name, jid in JOURNAL_ALIAS:
            if name in backup_cell and jid not in backups:
                backups.append(jid)

        stretch_ids = parse_journal_ids(stretch_cell)
        stretch = stretch_ids[0] if stretch_ids else meta["journal_stretch"]

        primary_ids = parse_journal_ids(primary_cell)
        primary = primary_ids[0] if primary_ids else meta["journal_primary"]

        risk_tags = []
        feasibility = meta["feasibility"]
        if "题目错误" in title or "误写" in title:
            risk_tags.append("题目待修")
            feasibility = "red"
        if method_id in {"art03", "art04", "art07"}:
            risk_tags.append("依赖复发/化疗信息完整性")
        if method_id == "art04":
            risk_tags.append("可能阴性结果需降档")

        datasets = extract_datasets(title, methods_detail)
        writing_style = writing.split("（")[0].strip() if writing else method_id

        intro = (
            f"本研究针对{cancer_zh}，采用「{writing_style}」路线。"
            f"核心方向：{direction}。"
            f"目标投稿质量：{meta['quality_target']}。"
        )

        paper = {
            "id": f"{cancer_id}_{method_id}",
            "serial": int(no),
            "cancer_id": cancer_id,
            "cancer_zh": cancer_zh,
            "method_id": method_id,
            "art_no": method_id,
            "title": title.replace(" 【题目错误：现稿误写为胰腺腺癌/GSE57495，投稿前须改为透明细胞肾癌及正确GEO】", "").strip(),
            "direction": direction,
            "methods_detail": methods_detail,
            "datasets": datasets,
            "disease": cancer_zh,
            "analysis_style": meta["analysis_style"],
            "writing_style": writing_style,
            "quality_target": meta["quality_target"],
            "journal_primary": primary,
            "journals_backup": backups,
            "journal_stretch": stretch,
            "feasibility": feasibility,
            "risk_tags": risk_tags,
            "intro": intro,
            "graphical_abstract": f"assets/ga/{cancer_id}_{method_id}.svg",
            "status": "data_ready",
        }
        papers.append(paper)

    OUT.write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(papers)} papers → {OUT}")


if __name__ == "__main__":
    main()
