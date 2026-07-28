# -*- coding: utf-8 -*-
"""Batch Nature-style schematic GAs for missing website papers (no fake data curves)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DATA = Path(__file__).resolve().parent
WEB = DATA.parent
GA = WEB / "assets" / "ga"
PAPERS = DATA / "papers.json"

W, H = 1400, 788

METHOD_LABEL = {
    "art01": ("Clinical + Transcriptome", "OS model · validation"),
    "art02": ("Clinical + Genomic", "Mutation · TMB · MMR"),
    "art03": ("Clinical + Transcriptome", "RFS / DFS model"),
    "art04": ("Risk × Chemotherapy", "Treatment interaction"),
    "art05": ("Cross-platform subtypes", "RNA-seq ↔ microarray"),
    "art06": ("Immune + TMB / MMR", "Integrated OS model"),
    "art07": ("Stage II/III subgroup", "RFS stratification"),
    "art08": ("Multi-model ML survival", "Cox · RSF · GBSA"),
}

PANELS = {
    "art01": ("Cohort", "Features", "Cox model", "Validate"),
    "art02": ("Cohort", "Mutations", "Model", "Validate"),
    "art03": ("Cohort", "Signature", "RFS model", "Validate"),
    "art04": ("Risk score", "Chemo", "Interaction", "Benefit"),
    "art05": ("RNA-seq", "Array", "Subtypes", "Agreement"),
    "art06": ("Immune", "TMB/MMR", "Integrate", "OS"),
    "art07": ("Stage II/III", "Features", "Subgroup", "RFS"),
    "art08": ("Cohort", "ML models", "Explain", "Compare"),
}


def palette(seed: str) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    h = hashlib.md5(seed.encode()).hexdigest()
    # soft navy/teal family with per-cancer hue shift
    base = int(h[:2], 16)
    navy = (20 + base % 30, 40 + base % 40, 70 + base % 50)
    teal = (15 + base % 20, 110 + base % 40, 120 + base % 40)
    coral = (180 + base % 40, 90 + base % 30, 90 + base % 40)
    return navy, teal, coral


def font(size: int) -> ImageFont.ImageFont:
    for name in (
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibril.ttf",
    ):
        p = Path(name)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def rounded(draw: ImageDraw.ImageDraw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def make_ga(paper: dict, out: Path) -> None:
    mid = paper.get("method_id") or paper.get("art_no") or "art01"
    title_en, subtitle = METHOD_LABEL.get(mid, ("Omics prognostic model", "Workflow schematic"))
    panels = PANELS.get(mid, ("Input", "Process", "Model", "Output"))
    cancer = paper.get("cancer_zh") or paper.get("disease") or paper["cancer_id"]
    navy, teal, coral = palette(paper["id"])

    img = Image.new("RGB", (W, H), (252, 253, 254))
    d = ImageDraw.Draw(img)

    # header bar
    d.rectangle((0, 0, W, 8), fill=teal)
    d.text((48, 36), cancer, fill=navy, font=font(36))
    d.text((48, 86), title_en, fill=teal, font=font(28))
    d.text((48, 126), subtitle, fill=(90, 110, 120), font=font(20))

    # workflow panels
    n = len(panels)
    margin = 48
    gap = 28
    usable = W - 2 * margin - gap * (n - 1)
    pw = usable // n
    top, bot = 200, 520
    centers = []
    for i, lab in enumerate(panels):
        x0 = margin + i * (pw + gap)
        x1 = x0 + pw
        fill = (232, 245, 243) if i % 2 == 0 else (236, 242, 248)
        rounded(d, (x0, top, x1, bot), 22, fill=fill, outline=teal, width=3)
        # icon circle
        cx = (x0 + x1) // 2
        cy = top + 110
        r = 42
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=teal if i < n - 1 else coral)
        d.text((cx - 10, cy - 16), str(i + 1), fill=(255, 255, 255), font=font(28))
        # label
        tw = d.textlength(lab, font=font(22))
        d.text((cx - tw / 2, bot - 70), lab, fill=navy, font=font(22))
        centers.append(cx)
        if i < n - 1:
            ax0 = x1 + 4
            ax1 = x1 + gap - 4
            midy = (top + bot) // 2
            d.line((ax0, midy, ax1, midy), fill=teal, width=4)
            d.polygon([(ax1, midy), (ax1 - 12, midy - 8), (ax1 - 12, midy + 8)], fill=teal)

    # bottom conceptual badges (empty — no fake stats)
    by = 580
    badges = ["Cohort lock", "Model fit", "Internal check", "Transparent reporting"]
    bw = (W - 2 * margin - 3 * 20) // 4
    for i, b in enumerate(badges):
        x0 = margin + i * (bw + 20)
        rounded(d, (x0, by, x0 + bw, by + 110), 16, fill=(255, 255, 255), outline=(200, 210, 218), width=2)
        d.ellipse((x0 + 18, by + 36, x0 + 48, by + 66), outline=teal, width=3)
        d.text((x0 + 60, by + 40), b, fill=(70, 90, 100), font=font(18))

    # footer
    d.text(
        (48, H - 48),
        "Graphical abstract · schematic only · no fabricated statistics",
        fill=(140, 155, 165),
        font=font(16),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="JPEG", quality=85, optimize=True)


def main() -> None:
    papers = json.loads(PAPERS.read_text(encoding="utf-8"))
    made = 0
    skip = 0
    for p in papers:
        out = GA / f"{p['id']}.jpg"
        if out.exists() and out.stat().st_size > 20_000:
            skip += 1
            continue
        make_ga(p, out)
        made += 1
    print(json.dumps({"made": made, "skipped_existing": skip, "total_papers": len(papers)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
