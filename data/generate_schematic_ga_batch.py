# -*- coding: utf-8 -*-
"""Nature-style schematic GAs for website papers (unique per id; no fake data)."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

DATA = Path(__file__).resolve().parent
WEB = DATA.parent
GA = WEB / "assets" / "ga"
PAPERS = DATA / "papers.json"
NEED = DATA / "need_ai_ga_round2.json"

W, H = 1536, 864

METHOD_LABEL = {
    "art01": ("Clinical + Transcriptome OS", "Cohort → Features → Model → Validate"),
    "art02": ("Clinical + Genomic OS", "Mutations · TMB · MMR → Model"),
    "art03": ("Clinical + Transcriptome RFS", "Signature → Recurrence model"),
    "art04": ("Risk × Chemotherapy", "Interaction benefit framework"),
    "art05": ("Cross-platform subtypes", "RNA-seq ↔ Microarray agreement"),
    "art06": ("Immune + TMB / MMR", "Integrated immune-genomic OS"),
    "art07": ("Stage II/III subgroup RFS", "Stage-restricted modeling"),
    "art08": ("Multi-model ML survival", "Cox · RSF · GBSA comparison"),
}

PANELS = {
    "art01": ("Cohort", "Features", "Cox model", "Validate"),
    "art02": ("Cohort", "Genomics", "Model", "Validate"),
    "art03": ("Cohort", "Signature", "RFS model", "Validate"),
    "art04": ("Risk", "Chemo", "Interact", "Benefit"),
    "art05": ("RNA-seq", "Array", "Subtypes", "κ check"),
    "art06": ("Immune", "TMB/MMR", "Integrate", "OS"),
    "art07": ("Stage II/III", "Features", "Subgroup", "RFS"),
    "art08": ("Inputs", "ML suite", "Explain", "Select"),
}


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    cands = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"]
    )
    for name in cands:
        if Path(name).exists():
            return ImageFont.truetype(name, size=size)
    return ImageFont.load_default()


def palette(seed: str):
    h = hashlib.md5(seed.encode()).hexdigest()
    a, b, c = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    navy = (18 + a % 28, 32 + b % 28, 58 + c % 40)
    teal = (12 + a % 18, 118 + b % 50, 124 + c % 40)
    coral = (190 + a % 40, 88 + b % 35, 92 + c % 35)
    mist = (244 + a % 8, 248, 250)
    return navy, teal, coral, mist


def rounded(draw, xy, r, fill=None, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def soft_shadow(base: Image.Image, box, radius=18, blur=10, alpha=55):
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + 4, y0 + 6, x1 + 4, y1 + 6), radius=radius, fill=(20, 30, 40, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def organ_blob(draw, cx, cy, r, fill, kind: str):
    """Very abstract organ mark — uniqueness without medical accuracy claims."""
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    if kind in {"lung", "blood"}:
        draw.ellipse((cx - r // 2, cy - r // 3, cx + r // 2, cy + r // 2), fill=(255, 255, 255, 60) if False else (255, 255, 255))
        # overwrite with smaller white disk for highlight
        draw.ellipse((cx - r // 3, cy - r // 2, cx - r // 12, cy - r // 6), fill=(255, 255, 255))
    elif kind in {"brain", "neural"}:
        for i in range(3):
            ang = i * 2.1
            x = cx + int(math.cos(ang) * r * 0.45)
            y = cy + int(math.sin(ang) * r * 0.45)
            draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(255, 255, 255))
    else:
        draw.ellipse((cx - r // 3, cy - r // 2, cx - r // 12, cy - r // 6), fill=(255, 255, 255))


def organ_kind(cancer_id: str) -> str:
    m = {
        "luad": "lung",
        "lusc": "lung",
        "aml": "blood",
        "dlbc": "blood",
        "gbm": "brain",
        "lgg": "brain",
        "nbl": "neural",
        "brca": "breast",
        "mbrca": "breast",
    }
    return m.get(cancer_id, "generic")


def make_ga(paper: dict, out: Path, force: bool = False) -> bool:
    if out.exists() and out.stat().st_size > 20_000 and not force:
        return False

    mid = paper.get("method_id") or "art01"
    title, subtitle = METHOD_LABEL.get(mid, ("Omics prognostic model", "Workflow schematic"))
    panels = PANELS.get(mid, ("Input", "Process", "Model", "Output"))
    cancer = paper.get("cancer_zh") or paper["cancer_id"]
    navy, teal, coral, mist = palette(paper["id"])

    img = Image.new("RGB", (W, H), mist)
    # subtle top wash
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for i in range(180):
        a = int(28 * (1 - i / 180))
        wd.line((0, i, W, i), fill=(teal[0], teal[1], teal[2], a))
    img = Image.alpha_composite(img.convert("RGBA"), wash).convert("RGB")
    d = ImageDraw.Draw(img)

    # top accent
    d.rectangle((0, 0, W, 10), fill=teal)

    # header card
    img = soft_shadow(img, (40, 36, W - 40, 168), radius=20, blur=8, alpha=40)
    d = ImageDraw.Draw(img)
    rounded(d, (40, 36, W - 40, 168), 20, fill=(255, 255, 255), outline=(220, 230, 236), width=2)
    organ_blob(d, 100, 102, 28, teal, organ_kind(paper["cancer_id"]))
    d.text((150, 58), cancer, fill=navy, font=font(34, bold=True))
    d.text((150, 104), title, fill=teal, font=font(24, bold=True))
    d.text((150, 136), subtitle, fill=(100, 120, 130), font=font(18))

    # workflow panels
    n = len(panels)
    margin, gap, top, bot = 48, 26, 210, 560
    usable = W - 2 * margin - gap * (n - 1)
    pw = usable // n
    for i, lab in enumerate(panels):
        x0 = margin + i * (pw + gap)
        x1 = x0 + pw
        fill = (236, 247, 245) if i % 2 == 0 else (238, 244, 250)
        img = soft_shadow(img, (x0, top, x1, bot), radius=24, blur=7, alpha=35)
        d = ImageDraw.Draw(img)
        rounded(d, (x0, top, x1, bot), 24, fill=fill, outline=teal if i < n - 1 else coral, width=3)
        cx, cy = (x0 + x1) // 2, top + 120
        rr = 46
        col = teal if i < n - 1 else coral
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col)
        # step glyph
        if mid == "art04" and i == 2:
            # interaction cross
            d.line((cx - 16, cy, cx + 16, cy), fill=(255, 255, 255), width=4)
            d.line((cx, cy - 16, cx, cy + 16), fill=(255, 255, 255), width=4)
        elif mid == "art08" and i == 1:
            for k, dy in enumerate((-14, 0, 14)):
                d.rounded_rectangle((cx - 18, cy + dy - 5, cx + 18, cy + dy + 5), 3, fill=(255, 255, 255))
        else:
            num = str(i + 1)
            tw = d.textlength(num, font=font(30, bold=True))
            d.text((cx - tw / 2, cy - 18), num, fill=(255, 255, 255), font=font(30, bold=True))
        tw = d.textlength(lab, font=font(22, bold=True))
        d.text((cx - tw / 2, bot - 78), lab, fill=navy, font=font(22, bold=True))
        # tiny empty chart placeholder
        bx0, by0 = x0 + 28, bot - 150
        bx1, by1 = x1 - 28, bot - 100
        rounded(d, (bx0, by0, bx1, by1), 8, fill=(255, 255, 255), outline=(190, 205, 212), width=2)
        d.line((bx0 + 10, by1 - 10, bx1 - 10, by1 - 10), fill=(200, 210, 218), width=2)
        d.line((bx0 + 10, by0 + 10, bx0 + 10, by1 - 10), fill=(200, 210, 218), width=2)
        if i < n - 1:
            ax0, ax1, midy = x1 + 3, x1 + gap - 3, (top + bot) // 2
            d.line((ax0, midy, ax1 - 8, midy), fill=teal, width=5)
            d.polygon([(ax1, midy), (ax1 - 14, midy - 9), (ax1 - 14, midy + 9)], fill=teal)

    # footer badges
    d = ImageDraw.Draw(img)
    badges = ["Locked split", "Transparent metrics", "No fabricated plots", "Reporting-ready"]
    by = 610
    bw = (W - 2 * margin - 3 * 18) // 4
    for i, b in enumerate(badges):
        x0 = margin + i * (bw + 18)
        rounded(d, (x0, by, x0 + bw, by + 100), 16, fill=(255, 255, 255), outline=(210, 220, 226), width=2)
        d.ellipse((x0 + 18, by + 34, x0 + 52, by + 68), outline=teal, width=3)
        d.text((x0 + 64, by + 40), b, fill=(70, 90, 105), font=font(18))

    d.text(
        (48, H - 42),
        "Graphical abstract · schematic only · no fabricated statistics",
        fill=(150, 165, 175),
        font=font(16),
    )
    # uniqueness mark (tiny, non-data)
    mark = hashlib.md5(paper["id"].encode()).hexdigest()[:6].upper()
    d.text((W - 120, H - 42), mark, fill=(180, 190, 198), font=font(14))

    out.parent.mkdir(parents=True, exist_ok=True)
    rgb = img.convert("RGB")
    if rgb.width > 1400:
        nh = int(rgb.height * 1400 / rgb.width)
        rgb = rgb.resize((1400, nh), Image.Resampling.LANCZOS)
    rgb.save(out, format="JPEG", quality=86, optimize=True)
    return True


def main() -> None:
    papers = json.loads(PAPERS.read_text(encoding="utf-8"))
    force_ids = set()
    if NEED.exists():
        force_ids = {p["id"] for p in json.loads(NEED.read_text(encoding="utf-8"))}
    made = skip = 0
    for p in papers:
        out = GA / f"{p['id']}.jpg"
        force = p["id"] in force_ids
        if make_ga(p, out, force=force):
            made += 1
        else:
            skip += 1
    print(json.dumps({"made_or_replaced": made, "kept_existing": skip, "forced": len(force_ids)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
