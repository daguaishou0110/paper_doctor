# -*- coding: utf-8 -*-
import json
import shutil
from pathlib import Path

from PIL import Image

src = Path(r"C:\Users\13594\.cursor\projects\d-hyf-freelance-work-niumayuan-2026\assets")
dst = Path(r"d:\hyf\freelance-work\niumayuan\2026\多癌种论文工厂\website\assets\ga")
papers = json.loads(
    Path(r"d:\hyf\freelance-work\niumayuan\2026\多癌种论文工厂\website\data\papers.json").read_text(encoding="utf-8")
)
art08 = [p for p in papers if p["method_id"] == "art08"]
synced = []
for p in art08:
    pid = p["id"]
    hits = sorted(src.glob(pid + "*.png"), key=lambda x: x.stat().st_mtime, reverse=True)
    if hits and hits[0].stat().st_size > 200000:
        Image.open(hits[0]).convert("RGB").save(dst / f"{pid}.jpg", "JPEG", quality=92, optimize=True)
        synced.append(pid)

# ensure base
if (src / "crc_art08.png").exists():
    Image.open(src / "crc_art08.png").convert("RGB").save(dst / "crc_art08.jpg", "JPEG", quality=92, optimize=True)
base = dst / "crc_art08.jpg"
filled = []
for p in art08:
    out = dst / f"{p['id']}.jpg"
    if p["id"] in synced:
        continue
    if base.exists():
        shutil.copy2(base, out)
        filled.append(p["id"])

# install into TeX for art08 only
import importlib.util

inst = Path(r"d:\hyf\freelance-work\niumayuan\2026\多癌种论文工厂\website\data\install_ga_into_tex.py")
spec = importlib.util.spec_from_file_location("inst", inst)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
ok = 0
for p in art08:
    ga = dst / f"{p['id']}.jpg"
    if not ga.exists():
        continue
    art = m.find_article_dir(p["cancer_id"], "art08")
    if art is None:
        # try direct path
        zh = p["cancer_zh"]
        cand = Path(r"d:\hyf\freelance-work\niumayuan\2026\多癌种论文工厂") / zh / "article08_multi_model_ml_prognostic"
        art = cand if cand.exists() else None
    if art is None:
        print("NOART", p["id"])
        continue
    # extend CANCER_DIR on the fly
    m.CANCER_DIR[p["cancer_id"]] = p["cancer_zh"]
    m.install_image(art, ga)
    m.patch_tex(art / "manuscript" / "manuscript.tex", "art08")
    ok += 1
print("synced_ai", synced)
print("filled", len(filled))
print("installed_tex", ok)
