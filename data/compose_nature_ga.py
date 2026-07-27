# -*- coding: utf-8 -*-
"""Compose Nature-style GAs from REAL paper figures + metrics (no fabricated plots)."""
from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT_WEB = Path(__file__).resolve().parents[1] / "assets" / "ga"
OUT_WEB.mkdir(parents=True, exist_ok=True)

CANCER_DIR = {
    "crc": "结直肠癌",
    "brca": "乳腺癌",
    "stad": "胃腺癌",
    "luad": "肺腺癌",
    "lusc": "肺鳞癌",
    "lihc": "肝细胞癌",
    "paad": "胰腺腺癌",
    "hnsc": "头颈鳞癌",
    "kirc": "肾透明细胞癌",
}
CANCER_EN = {
    "crc": "Colorectal Cancer",
    "brca": "Breast Cancer",
    "stad": "Gastric Adenocarcinoma",
    "luad": "Lung Adenocarcinoma",
    "lusc": "Lung Squamous Cell Carcinoma",
    "lihc": "Hepatocellular Carcinoma",
    "paad": "Pancreatic Adenocarcinoma",
    "hnsc": "Head & Neck Squamous Cell Carcinoma",
    "kirc": "Clear Cell Renal Cell Carcinoma",
}
METHOD_TITLE = {
    "art01": "Clinical–Transcriptomic OS Model",
    "art02": "Clinical–Genomic OS Model",
    "art03": "Clinical–Transcriptomic RFS Model",
    "art04": "Risk × Chemotherapy Interaction",
    "art05": "Cross-Platform Subtype Validation",
    "art06": "Clinical–Immune–Genomic OS Model",
    "art07": "Stage II/III Subgroup RFS Model",
}
METHOD_STEPS = {
    "art01": ["Cohort", "Feature lock", "Cox model", "Validation"],
    "art02": ["Cohort", "Mut/TMB/MMR", "Cox model", "Validation"],
    "art03": ["RFS cohort", "Feature lock", "Cox model", "Validation"],
    "art04": ["Risk score", "Chemo status", "Interaction", "Subgroup KM"],
    "art05": ["RNA-seq", "Microarray", "Mapping", "Agreement"],
    "art06": ["Immune", "TMB/MMR", "Integrated", "Validation"],
    "art07": ["Stage II/III", "Feature lock", "Cox model", "Validation"],
}
CRC_SPECIAL = {
    "art05": "article05_cms_subtyping_validation",
    "art07": "article07_stage23_rfs_model",
}

# palette
BG = (255, 255, 255)
INK = (21, 32, 40)
SOFT = (74, 91, 104)
TEAL = (15, 110, 106)
TEAL_SOFT = (216, 239, 237)
LINE = (213, 222, 230)
CORAL = (196, 92, 74)

W, H = 1600, 900


def font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def find_article(cid: str, mid: str) -> Path | None:
    cr = ROOT / CANCER_DIR[cid]
    if not cr.exists():
        return None
    if cid == "crc" and mid in CRC_SPECIAL:
        p = cr / CRC_SPECIAL[mid]
        return p if p.exists() else None
    ms = sorted(cr.glob(f"article{mid[-2:]}_*"))
    return ms[0] if ms else None


def load_summary(article: Path) -> dict:
    hits = [
        p
        for p in article.rglob("analysis_summary.json")
        if ".venv" not in str(p) and "site-packages" not in str(p)
    ]
    if not hits:
        return {}
    try:
        return json.loads(hits[0].read_text(encoding="utf-8"))
    except Exception:
        return {}


def fmt_p(p: float) -> str:
    if p is None or (isinstance(p, float) and (math.isnan(p) or math.isinf(p))):
        return ""
    if p < 1e-4:
        return f"{p:.1e}"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.3f}"


def pick_metrics(mid: str, s: dict) -> list[tuple[str, str]]:
    """Return real metric badges only; skip missing/empty."""
    out: list[tuple[str, str]] = []

    def add(label: str, key_candidates: list[str], fmt=" {:.3f}"):
        for k in key_candidates:
            if k in s and s[k] is not None and not isinstance(s[k], (dict, list)):
                try:
                    v = float(s[k])
                except Exception:
                    out.append((label, str(s[k])))
                    return
                if "p" in label.lower() or "logrank" in k.lower() or k.endswith("_p"):
                    out.append((label, fmt_p(v)))
                elif abs(v) >= 100:
                    out.append((label, f"{v:.0f}"))
                else:
                    out.append((label, fmt.format(v).strip()))
                return

    add("n", ["n_merged", "n_total", "train_n", "tcga_n"])
    if "n_test" in s:
        add("n_test", ["n_test"])
    if mid in {"art01", "art02", "art03", "art06", "art07"}:
        add(
            "C-index clin",
            ["c_index_test_clinical", "test_cindex_clinical", "cindex_clinical"],
        )
        add(
            "C-index full",
            [
                "c_index_test_full",
                "test_cindex_integrated",
                "test_cindex_genomic",
                "cindex_integrated",
                "cindex_immune_tmb",
            ],
        )
        add("ΔC-index", ["delta_c_index_test", "delta_cindex"])
        add("log-rank p", ["logrank_p_test", "logrank_p", "logrank_p_all"])
    if mid == "art04":
        add("C-index", ["prognostic_cindex_test"])
        add("Interaction HR", ["interaction_hr_test", "interaction_hr"])
        add("Interaction p", ["interaction_p_test", "interaction_p"])
    if mid == "art05":
        add("κ", ["kappa"])
        add("Accuracy", ["accuracy"])
        add("TCGA n", ["tcga_n"])
        add("GEO n", ["gse_n", "gse_valid_n"])
    return out[:5]


def pick_figure(article: Path, mid: str) -> Path | None:
    fig = article / "figures" / "main"
    if not fig.exists():
        return None
    preferred = {
        "art01": ["fig_km_test.png", "fig_model_comparison.png", "fig_km_all.png"],
        "art02": ["fig_km_test.png", "fig_model_comparison.png"],
        "art03": ["fig_km_rfs_test.png", "fig_model_comparison.png"],
        "art04": [
            "fig_km_interaction_four_groups.png",
            "fig_km_chemo_high_risk.png",
            "fig_km_chemo_low_risk.png",
        ],
        "art05": ["fig_km_cms_tcga.png", "fig_km_cms_gse.png"],
        "art06": ["fig_km_test.png", "fig_model_comparison.png"],
        "art07": ["fig_km_rfs_test.png", "fig_model_comparison.png"],
    }
    for name in preferred.get(mid, []):
        p = fig / name
        if p.exists():
            return p
    # fallback any km / comparison except scheme/ga/bak
    for p in sorted(fig.glob("fig_*.png")):
        if any(x in p.name for x in ["scheme", "graphical", "bak", "nomogram"]):
            continue
        if "km" in p.name or "comparison" in p.name or "roc" in p.name:
            return p
    return None


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def compose_one(cid: str, mid: str) -> Path | None:
    article = find_article(cid, mid)
    if article is None:
        return None
    summary = load_summary(article)
    metrics = pick_metrics(mid, summary)
    real_fig = pick_figure(article, mid)
    has_real_visual = real_fig is not None and len(metrics) > 0

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    f_title = font(36, True)
    f_sub = font(20, False)
    f_step = font(18, True)
    f_badge = font(16, True)
    f_small = font(14, False)

    # header
    title = f"{CANCER_EN[cid]}"
    subtitle = METHOD_TITLE[mid]
    draw.text((48, 36), title, fill=INK, font=f_title)
    draw.text((48, 84), subtitle, fill=TEAL, font=f_sub)
    draw.rectangle((48, 118, 220, 124), fill=TEAL)

    # left workflow steps
    steps = METHOD_STEPS[mid]
    x0, y0 = 48, 170
    box_w, box_h = 200, 70
    gap = 28
    for i, step in enumerate(steps):
        x = x0
        y = y0 + i * (box_h + gap)
        rounded_rect(draw, (x, y, x + box_w, y + box_h), 14, TEAL_SOFT, TEAL, 2)
        draw.text((x + 18, y + 22), step, fill=TEAL, font=f_step)
        if i < len(steps) - 1:
            cx = x + box_w // 2
            draw.line((cx, y + box_h, cx, y + box_h + gap), fill=TEAL, width=3)
            draw.polygon(
                [(cx - 7, y + box_h + gap - 10), (cx + 7, y + box_h + gap - 10), (cx, y + box_h + gap)],
                fill=TEAL,
            )

    # right panel: real figure OR schematic note
    panel = (300, 150, 1550, 820)
    rounded_rect(draw, panel, 18, (250, 252, 253), LINE, 2)

    if real_fig is not None:
        fig = Image.open(real_fig).convert("RGB")
        max_w, max_h = 1180, 560
        fig.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        fx = panel[0] + (panel[2] - panel[0] - fig.width) // 2
        fy = panel[1] + 24
        img.paste(fig, (fx, fy))
        caption = "Embedded from this article's locked analysis output"
        draw.text((panel[0] + 24, panel[3] - 36), caption, fill=SOFT, font=f_small)
    else:
        msg = "Schematic overview only — result figure not available yet."
        draw.text((panel[0] + 40, panel[1] + 280), msg, fill=SOFT, font=f_sub)

    # metric badges from REAL summary only
    bx, by = 300, 830
    if metrics and has_real_visual:
        for i, (lab, val) in enumerate(metrics):
            text = f"{lab}: {val}"
            tw = draw.textlength(text, font=f_badge)
            pad = 14
            x1 = bx
            y1 = by
            # wrap to next line if needed
            if x1 + tw + 2 * pad > 1540:
                bx = 300
                by += 44
                x1, y1 = bx, by
            rounded_rect(draw, (x1, y1, x1 + tw + 2 * pad, y1 + 34), 10, (255, 255, 255), TEAL, 2)
            draw.text((x1 + pad, y1 + 7), text, fill=INK, font=f_badge)
            bx = x1 + tw + 2 * pad + 12
    elif not metrics:
        note = "No numeric badges shown (metrics unavailable)."
        draw.text((300, 840), note, fill=SOFT, font=f_small)

    # footer honesty note
    foot = "Metrics and plots are taken from this article's analysis outputs; no fabricated statistics."
    draw.text((48, 870), foot, fill=SOFT, font=f_small)

    out = OUT_WEB / f"{cid}_{mid}.jpg"
    img.save(out, format="JPEG", quality=90, optimize=True)
    return out


def install_into_article(cid: str, mid: str, jpg: Path) -> None:
    article = find_article(cid, mid)
    if article is None:
        return
    fig_dir = article / "figures" / "main"
    fig_dir.mkdir(parents=True, exist_ok=True)
    png = fig_dir / "fig_model_scheme.png"
    # backup once
    if png.exists() and not (fig_dir / "fig_model_scheme.bak.png").exists():
        shutil.copy2(png, fig_dir / "fig_model_scheme.bak.png")
    im = Image.open(jpg).convert("RGB")
    im.save(png, format="PNG", optimize=True)
    shutil.copy2(jpg, fig_dir / "fig_graphical_abstract.jpg")


def main():
    ok = 0
    for cid in CANCER_DIR:
        for i in range(1, 8):
            mid = f"art0{i}"
            path = compose_one(cid, mid)
            if path:
                install_into_article(cid, mid, path)
                print("OK", path.name)
                ok += 1
            else:
                print("FAIL", f"{cid}_{mid}")
    print("done", ok)


if __name__ == "__main__":
    main()
