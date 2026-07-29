# 公卫队列产品线（epi）

与肿瘤组学线并行。写法：`epi01–epi04`。数据主源：CHARLS + 城市级暴露（RUI/PM/NDVI 等）。

## 成稿包

| ID | 写法 | 状态 | 说明 |
|----|------|------|------|
| `skoa_epi01` | epi01 | 成稿（已有） | `case/BMC_...docx` 为投刊正文；本目录可放副本 |
| `htn_epi01` | epi01 | 成稿骨架 | 非骨肌换病种示范；**结果数字待 CHARLS 复跑写入** |
| `dm_epi03` | epi03 | 成稿骨架 | 纵向发病示范；**随访表与 HR 待多波次清洗写入** |

## 跑数

1. 将 CHARLS 用户下载的基线/随访与城市暴露表放到各篇 `data/`（勿提交隐私与未授权数据）。
2. 运行对应 `code/run_analysis.py`（或 R 脚本）生成 `results/*.csv|json`。
3. 用 `code/fill_results_into_manuscript.py`（若有）把占位符替换进正文。

## 站点

`website/data/build_epi_line.py` 维护选题卡；成稿状态在 `papers.json` 的 `status=manuscript`。
