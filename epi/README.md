# 公卫队列产品线（epi）

与肿瘤组学线并行。写法：`epi01–epi04`。数据主源：CHARLS + 城市级暴露（RUI/PM/NDVI 等）。

## 成稿包

| ID | 写法 | 状态 | 说明 |
|----|------|------|------|
| `skoa_epi01` | epi01 | 成稿（已有） | `case/BMC_...docx` 为投刊正文 |
| `htn_epi01` | epi01 | 成稿骨架 | 非骨肌换病种；结果占位待 CHARLS |
| `dm_epi03` | epi03 | 成稿骨架 | 纵向发病；HR 待多波次写入 |

站点货架公卫线约 **42** 篇选题（3 成稿 + 39 可用），覆盖 12 病种 × epi01–04；扩产脚本：`website/data/expand_epi_catalog.py`。

## 跑数

1. 将 CHARLS 用户下载的基线/随访与城市暴露表放到各篇 `data/`（勿提交隐私与未授权数据）。
2. 运行对应 `code/run_analysis.py`（或 R 脚本）生成 `results/*.csv|json`。
3. 用 `code/fill_results_into_manuscript.py`（若有）把占位符替换进正文。

## 站点

`website/data/build_epi_line.py` 维护选题卡；成稿状态在 `papers.json` 的 `status=manuscript`。
