# -*- coding: utf-8 -*-
"""Sync fresh PNGs from Cursor assets → website/ga, then JPEG compress."""
from pathlib import Path
import json
from PIL import Image

cursor = Path(r"C:\Users\13594\.cursor\projects\d-hyf-freelance-work-niumayuan-2026\assets")
dst = Path(__file__).resolve().parents[1] / "assets" / "ga"
papers = json.loads((Path(__file__).resolve().parent / "papers.json").read_text(encoding="utf-8"))
ids = {p["id"] for p in papers}

copied = 0
for pid in sorted(ids):
    src = cursor / f"{pid}.png"
    if not src.exists():
        print("MISSING PNG", pid)
        continue
    (dst / f"{pid}.png").write_bytes(src.read_bytes())
    copied += 1
print("copied_png", copied)

total = 0
for pid in sorted(ids):
    png = dst / f"{pid}.png"
    jpg = dst / f"{pid}.jpg"
    im = Image.open(png).convert("RGB")
    w, h = im.size
    if w > 1400:
        im = im.resize((1400, int(h * 1400 / w)), Image.Resampling.LANCZOS)
    im.save(jpg, format="JPEG", quality=82, optimize=True)
    total += jpg.stat().st_size
    png.unlink(missing_ok=True)

for p in papers:
    p["graphical_abstract"] = f"assets/ga/{p['id']}.jpg"
(Path(__file__).resolve().parent / "papers.json").write_text(
    json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("jpg_MB", round(total / 1e6, 1), "count", len(list(dst.glob("*.jpg"))))
