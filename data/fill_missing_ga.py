# -*- coding: utf-8 -*-
import json
import shutil
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
WEB = Path(__file__).resolve().parents[1]
DATA = WEB / "data"
GA = WEB / "assets" / "ga"

FALLBACK_SRC = {
    "coad": "crc",
    "read": "crc",
    "thca": "hnsc",
    "kirp": "kirc",
    "kich": "kirc",
    "chol": "lihc",
    "meso": "luad",
    "lgg": "gbm",
    "tgct": "prad",
    "uvm": "skcm",
    "ucs": "ucec",
}


def make_placeholder(pid: str, cancer_zh: str, mid: str, out: Path) -> None:
    im = Image.new("RGB", (1536, 1024), "#f7fbfb")
    d = ImageDraw.Draw(im)
    d.rectangle([48, 48, 1488, 976], outline="#cfe0de", width=3, fill="#ffffff")
    d.text((80, 100), cancer_zh, fill="#152028")
    d.text((80, 180), mid, fill="#0f6e6a")
    d.text((80, 260), "Study overview schematic (placeholder)", fill="#4a5b68")
    im.save(out, "JPEG", quality=88, optimize=True)


def main() -> None:
    papers = json.loads((DATA / "papers.json").read_text(encoding="utf-8"))
    missing = []
    for p in papers:
        out = GA / f"{p['id']}.jpg"
        if out.exists():
            continue
        missing.append(p)
        cid = p["cancer_id"]
        src_cid = FALLBACK_SRC.get(cid)
        src = GA / f"{src_cid}_{p['method_id']}.jpg" if src_cid else None
        if src and src.exists():
            shutil.copy2(src, out)
            print("COPY", src.name, "→", out.name)
        else:
            make_placeholder(p["id"], p["cancer_zh"], p["method_id"], out)
            print("PLACEHOLDER", out.name)
    print("filled", len(missing), "by cancer", dict(Counter(p["cancer_id"] for p in missing)))


if __name__ == "__main__":
    main()
