# -*- coding: utf-8 -*-
"""
Nature-style graphical abstracts:
- Main visual = schematic workflow (journal GA look)
- Any numbers / mini-charts MUST come from this article's real outputs
- Do not invent KM/ROC/p-values
"""
from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

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
    "art01": "Clinical–Transcriptomic OS",
    "art02": "Clinical–Genomic OS",
    "art03": "Clinical–Transcriptomic RFS",
    "art04": "Risk × Chemotherapy Interaction",
    "art05": "Cross-Platform Subtyping",
    "art06": "Immune–Genomic OS",
    "art07": "Stage II/III Subgroup RFS",
}
# schematic panel labels (no fabricated stats)
PANELS = {
    "art01": [("Cohort", "Clinical + RNA"), ("Lock", "Train-only select"), ("Model", "Ridge Cox"), ("Check", "Locked test")],
    "art02": [("Cohort", "Clinical"), ("Genome", "Mut / TMB / MMR"), ("Model", "Cox"), ("Check", "Validation")],
    "art03": [("Cohort", "RFS endpoint"), ("Lock", "Train-only"), ("Model", "Cox"), ("Check", "Locked test")],
    "art04": [("Score", "Transcriptomic risk"), ("Treat", "Chemo ±"), ("Test", "Interaction"), ("Readout", "Subgroups")],
    "art05": [("RNA-seq", "Platform A"), ("Array", "Platform B"), ("Map", "Subtype call"), ("Agree", "Consistency")],
    "art06": [("Immune", "IFN-γ / infiltrate"), ("Genome", "TMB / MMR"), ("Model", "Integrated"), ("Check", "Validation")],
    "art07": [("Filter", "Stage II/III"), ("Lock", "Train-only"), ("Model", "Cox"), ("Check", "Locked test")],
}
CRC_SPECIAL = {
    "art05": "article05_cms_subtyping_validation",
    "art07": "article07_stage23_rfs_model",
}

BG = (255, 255, 255)
INK = (21, 32, 40)
SOFT = (90, 105, 118)
TEAL = (15, 110, 106)
TEAL_SOFT = (232, 245, 243)
TEAL_MID = (168, 214, 209)
LINE = (210, 220, 228)
CORAL = (184, 90, 72)
NAVY = (30, 58, 95)

W, H = 1600, 900


def font(size: int, bold: bool = False):
    paths = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for p in paths:
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
    return f"{p:.3f}"


def pick_metrics(mid: str, s: dict) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []

    def add(label: str, keys: list[str]):
        for k in keys:
            if k not in s or s[k] is None or isinstance(s[k], (dict, list)):
                continue
            try:
                v = float(s[k])
            except Exception:
                out.append((label, str(s[k])))
                return
            if "p" in label.lower() or k.endswith("_p") or "logrank" in k:
                out.append((label, fmt_p(v)))
            elif abs(v) >= 100:
                out.append((label, f"{int(round(v))}"))
            else:
                out.append((label, f"{v:.3f}"))
            return

    add("n", ["n_merged", "tcga_n", "train_n"])
    if mid in {"art01", "art02", "art03", "art06", "art07"}:
        add("C-index clin", ["c_index_test_clinical", "test_cindex_clinical", "cindex_clinical"])
        add(
            "C-index model",
            [
                "c_index_test_full",
                "test_cindex_integrated",
                "test_cindex_genomic",
                "cindex_integrated",
                "cindex_immune_tmb",
            ],
        )
        add("ΔC", ["delta_c_index_test", "delta_cindex"])
    if mid == "art04":
        add("C-index", ["prognostic_cindex_test"])
        add("Int. HR", ["interaction_hr_test", "interaction_hr"])
        add("Int. p", ["interaction_p_test", "interaction_p"])
    if mid == "art05":
        add("κ", ["kappa"])
        add("Acc.", ["accuracy"])
        add("GEO n", ["gse_n", "gse_valid_n"])
    return out[:4]


def pick_figure(article: Path, mid: str) -> Path | None:
    fig = article / "figures" / "main"
    if not fig.exists():
        return None
    preferred = {
        "art01": ["fig_km_test.png", "fig_model_comparison.png"],
        "art02": ["fig_km_test.png", "fig_model_comparison.png"],
        "art03": ["fig_km_rfs_test.png", "fig_model_comparison.png"],
        "art04": ["fig_km_interaction_four_groups.png", "fig_km_chemo_high_risk.png"],
        "art05": ["fig_km_cms_tcga.png", "fig_km_cms_gse.png"],
        "art06": ["fig_km_test.png", "fig_model_comparison.png"],
        "art07": ["fig_km_rfs_test.png", "fig_model_comparison.png"],
    }
    for name in preferred.get(mid, []):
        p = fig / name
        if p.exists():
            return p
    return None


def draw_icon(draw: ImageDraw.ImageDraw, kind: str, cx: int, cy: int):
    """Simple flat icons — schematic only."""
    if kind in {"Cohort", "Filter"}:
        draw.ellipse((cx - 22, cy - 28, cx + 22, cy + 10), outline=TEAL, width=3)
        draw.ellipse((cx - 34, cy + 8, cx + 34, cy + 34), outline=TEAL, width=3)
    elif kind in {"Lock", "Map"}:
        draw.rounded_rectangle((cx - 20, cy - 8, cx + 20, cy + 24), 6, outline=TEAL, width=3)
        draw.arc((cx - 14, cy - 28, cx + 14, cy), 0, 180, fill=TEAL, width=3)
    elif kind in {"Model", "Test"}:
        draw.polygon([(cx, cy - 28), (cx + 28, cy), (cx, cy + 28), (cx - 28, cy)], outline=TEAL, width=3)
    elif kind in {"Check", "Readout", "Agree"}:
        draw.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), outline=TEAL, width=3)
        draw.line((cx - 12, cy + 2, cx - 2, cy + 12), fill=CORAL, width=4)
        draw.line((cx - 2, cy + 12, cx + 14, cy - 10), fill=CORAL, width=4)
    elif kind in {"Genome", "RNA-seq", "Array"}:
        draw.line((cx - 20, cy - 20, cx + 20, cy + 20), fill=TEAL, width=3)
        draw.line((cx - 20, cy + 20, cx + 20, cy - 20), fill=CORAL, width=3)
        draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), outline=NAVY, width=2)
    elif kind in {"Immune", "Score", "Treat"}:
        draw.rounded_rectangle((cx - 24, cy - 20, cx + 24, cy + 20), 8, outline=TEAL, width=3)
        draw.line((cx - 10, cy, cx + 10, cy), fill=CORAL, width=3)
        draw.line((cx, cy - 10, cx, cy + 10), fill=CORAL, width=3)
    else:
        draw.rounded_rectangle((cx - 24, cy - 18, cx + 24, cy + 18), 8, outline=TEAL, width=3)


def compose_one(cid: str, mid: str) -> Path | None:
    article = find_article(cid, mid)
    if article is None:
        return None
    summary = load_summary(article)
    metrics = pick_metrics(mid, summary)
    real_fig = pick_figure(article, mid)

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    f_title = font(40, True)
    f_sub = font(22, False)
    f_panel = font(20, True)
    f_desc = font(15, False)
    f_badge = font(16, True)
    f_tiny = font(13, False)

    # header
    draw.text((56, 40), CANCER_EN[cid], fill=INK, font=f_title)
    draw.text((56, 92), f"Graphical Abstract  ·  {METHOD_TITLE[mid]}", fill=TEAL, font=f_sub)
    draw.rectangle((56, 130, 260, 136), fill=TEAL)

    # main schematic strip (Nature GA style)
    panels = PANELS[mid]
    n = len(panels)
    left, right = 56, 1544
    top, bottom = 180, 520
    total_w = right - left
    gap = 28
    pw = (total_w - gap * (n - 1)) // n
    for i, (name, desc) in enumerate(panels):
        x1 = left + i * (pw + gap)
        y1 = top
        x2 = x1 + pw
        y2 = bottom
        draw.rounded_rectangle((x1, y1, x2, y2), 22, fill=TEAL_SOFT, outline=TEAL_MID, width=2)
        # icon
        draw_icon(draw, name, (x1 + x2) // 2, y1 + 110)
        # labels
        tw = draw.textlength(name, font=f_panel)
        draw.text(((x1 + x2) / 2 - tw / 2, y1 + 200), name, fill=INK, font=f_panel)
        dw = draw.textlength(desc, font=f_desc)
        draw.text(((x1 + x2) / 2 - dw / 2, y1 + 240), desc, fill=SOFT, font=f_desc)
        if i < n - 1:
            ax = x2 + 4
            ay = (y1 + y2) // 2
            draw.line((ax, ay, ax + gap - 8, ay), fill=TEAL, width=4)
            draw.polygon([(ax + gap - 8, ay - 8), (ax + gap - 8, ay + 8), (ax + gap + 2, ay)], fill=TEAL)

    # bottom area: real metrics + optional SMALL real inset
    band_top = 560
    draw.rounded_rectangle((56, band_top, 1544, 860), 20, fill=(250, 252, 253), outline=LINE, width=2)

    # left text block
    draw.text((80, band_top + 24), "Evidence from this article (not fabricated)", fill=TEAL, font=f_panel)

    bx, by = 80, band_top + 70
    if metrics:
        for lab, val in metrics:
            text = f"{lab}  {val}"
            tw = draw.textlength(text, font=f_badge)
            draw.rounded_rectangle((bx, by, bx + tw + 28, by + 36), 18, fill=BG, outline=TEAL, width=2)
            draw.text((bx + 14, by + 8), text, fill=INK, font=f_badge)
            bx += tw + 40
            if bx > 980:
                bx = 80
                by += 48
    else:
        draw.text((80, by), "Numeric badges omitted — metrics unavailable in analysis_summary.", fill=SOFT, font=f_desc)

    # small real figure inset (secondary, not the whole GA)
    if real_fig is not None:
        inset = Image.open(real_fig).convert("RGB")
        inset.thumbnail((480, 250), Image.Resampling.LANCZOS)
        # white frame
        ix, iy = 1020, band_top + 40
        frame = Image.new("RGB", (inset.width + 16, inset.height + 16), BG)
        frame.paste(inset, (8, 8))
        img.paste(frame, (ix, iy))
        draw.rectangle((ix, iy, ix + frame.width, iy + frame.height), outline=LINE, width=2)
        draw.text((ix, iy + frame.height + 6), "Inset: real result panel from this paper", fill=SOFT, font=f_tiny)
    else:
        draw.text((1020, band_top + 120), "Schematic only — no result inset yet.", fill=SOFT, font=f_desc)

    draw.text(
        (56, 872),
        "Nature-style schematic workflow; any numbers/inset plots are taken from this article’s analysis outputs.",
        fill=SOFT,
        font=f_tiny,
    )

    out = OUT_WEB / f"{cid}_{mid}.jpg"
    img.save(out, quality=92, optimize=True)
    return out


def install_into_article(cid: str, mid: str, jpg: Path) -> None:
    article = find_article(cid, mid)
    if article is None:
        return
    fig_dir = article / "figures" / "main"
    fig_dir.mkdir(parents=True, exist_ok=True)
    png = fig_dir / "fig_model_scheme.png"
    if png.exists() and not (fig_dir / "fig_model_scheme.bak.png").exists():
        shutil.copy2(png, fig_dir / "fig_model_scheme.bak.png")
    Image.open(jpg).convert("RGB").save(png, format="PNG", optimize=True)
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
