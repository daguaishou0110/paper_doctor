# -*- coding: utf-8 -*-
"""Place Nature-style GAs into each paper's figures/main and TeX Study Overview."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
GA_DIR = Path(__file__).resolve().parents[1] / "assets" / "ga"

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
    "blca": "膀胱尿路上皮癌",
    "esca": "食管癌",
    "ov": "卵巢浆液性癌",
}

# CRC uses non-standard article folder names for art05/art07
CRC_SPECIAL = {
    "art05": "article05_cms_subtyping_validation",
    "art07": "article07_stage23_rfs_model",
}

CAPTIONS = {
    "art01": "Graphical abstract: Nature-style schematic of the clinical--transcriptomic OS modelling workflow.",
    "art02": "Graphical abstract: Nature-style schematic of the clinical--genomic OS modelling workflow.",
    "art03": "Graphical abstract: Nature-style schematic of the clinical--transcriptomic RFS modelling workflow.",
    "art04": "Graphical abstract: Nature-style schematic of the risk-stratified adjuvant chemotherapy benefit workflow.",
    "art05": "Graphical abstract: Nature-style schematic of the cross-platform molecular subtyping validation workflow.",
    "art06": "Graphical abstract: Nature-style schematic of the immune--genomic OS modelling workflow.",
    "art07": "Graphical abstract: Nature-style schematic of the stage II/III subgroup RFS modelling workflow.",
}


def find_article_dir(cancer_id: str, method_id: str) -> Path | None:
    cancer_root = ROOT / CANCER_DIR[cancer_id]
    if not cancer_root.exists():
        return None
    if cancer_id == "crc" and method_id in CRC_SPECIAL:
        p = cancer_root / CRC_SPECIAL[method_id]
        return p if p.exists() else None
    art_no = method_id  # art01 ...
    matches = sorted(cancer_root.glob(f"article{art_no[-2:]}_*"))
    # also try article01_ style with full method slug prefix
    if not matches:
        matches = sorted(
            p for p in cancer_root.glob("article*") if p.is_dir() and p.name.startswith(f"article{art_no[-2:]}")
        )
    return matches[0] if matches else None


def install_image(article_dir: Path, ga_jpg: Path) -> Path:
    fig_dir = article_dir / "figures" / "main"
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_png = fig_dir / "fig_model_scheme.png"
    out_jpg = fig_dir / "fig_graphical_abstract.jpg"
    # backup existing scheme once
    if out_png.exists() and not (fig_dir / "fig_model_scheme.bak.png").exists():
        shutil.copy2(out_png, fig_dir / "fig_model_scheme.bak.png")
    im = Image.open(ga_jpg).convert("RGB")
    im.save(out_png, format="PNG", optimize=True)
    shutil.copy2(ga_jpg, out_jpg)
    return out_png


def patch_tex(tex_path: Path, method_id: str) -> bool:
    if not tex_path.exists():
        return False
    text = tex_path.read_text(encoding="utf-8")
    caption = CAPTIONS.get(method_id, "Graphical abstract of the study overview pipeline.")
    new_text, n = re.subn(
        r"(\\includegraphics\[width=0\.95\\linewidth\]\{fig_model_scheme\.png\}\s*"
        r"\\caption\{)([^}]*)(\}\s*\\label\{fig:model_scheme\})",
        rf"\1{caption}\3",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        # try looser caption replace near fig_model_scheme
        new_text, n = re.subn(
            r"(\\includegraphics\[width=0\.95\\linewidth\]\{fig_model_scheme\.png\}\s*\\caption\{)([^}]*)(\})",
            rf"\1{caption}\3",
            text,
            count=1,
        )
    if n == 0:
        return False
    tex_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    ok = fail = skip = 0
    for ga in sorted(GA_DIR.glob("*_art0*.jpg")):
        pid = ga.stem  # crc_art01
        cancer_id, method_id = pid.split("_", 1)
        if cancer_id not in CANCER_DIR:
            print("SKIP_UNKNOWN", pid)
            skip += 1
            continue
        article = find_article_dir(cancer_id, method_id)
        if article is None:
            print("NO_ARTICLE", pid)
            fail += 1
            continue
        install_image(article, ga)
        tex = article / "manuscript" / "manuscript.tex"
        patched = patch_tex(tex, method_id)
        print("OK" if patched else "IMG_ONLY", pid, "→", article.name, "patched" if patched else "tex_not_patched")
        ok += 1
    print(f"done ok={ok} fail={fail} skip={skip}")


if __name__ == "__main__":
    main()
