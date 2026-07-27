# -*- coding: utf-8 -*-
from pathlib import Path
import json
from PIL import Image

root = Path(__file__).resolve().parents[1]
dst = root / "assets" / "ga"
papers_path = root / "data" / "papers.json"
papers = json.loads(papers_path.read_text(encoding="utf-8"))
ids = {p["id"] for p in papers}
total = 0
for pid in sorted(ids):
    png = dst / f"{pid}.png"
    jpg = dst / f"{pid}.jpg"
    src = png if png.exists() else jpg
    if not src.exists():
        print("MISSING", pid)
        continue
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w > 1400:
        im = im.resize((1400, int(h * 1400 / w)), Image.Resampling.LANCZOS)
    im.save(jpg, format="JPEG", quality=82, optimize=True)
    total += jpg.stat().st_size
    if png.exists():
        png.unlink()

for f in list(dst.glob("*")):
    if f.suffix.lower() in {".png", ".jpg"} and f.stem not in ids:
        print("removed", f.name)
        f.unlink()

for p in papers:
    p["graphical_abstract"] = f"assets/ga/{p['id']}.jpg"
papers_path.write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")
print("jpg_MB", round(total / 1e6, 1), "count", len(list(dst.glob("*.jpg"))))
