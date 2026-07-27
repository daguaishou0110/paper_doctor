# 多癌种论文工厂 · 选刊选题决策台（网站）

静态原型：写法百科 → 期刊情报 → 病症货架。

## 在线访问（Render）

详见 [DEPLOY_RENDER.md](./DEPLOY_RENDER.md)。

简要：把本目录推到 GitHub → Render 选 **New → Static Site** → Build 留空、Publish Directory 填 `.` → 得到 `https://xxx.onrender.com`。

## 本地预览

必须用静态服务器打开（`fetch` 读 JSON，不能直接双击 `index.html`）：

```bash
cd website
python serve.py
```

浏览器打开：http://127.0.0.1:18080/

## 目录

```
website/
├── index.html
├── assets/app.css
├── assets/app.js
└── data/
    ├── FIELD_DICTIONARY.md   # 字段字典
    ├── meta.json
    ├── methods.json          # 7 种写法
    ├── journals.json         # 期刊情报
    ├── cancers.json          # 9 个癌种
    ├── papers.json           # 63 篇选题
    └── build_papers.py       # 从总表重新生成 papers.json
```

## 当前进度

- [x] Step 1：字段字典 + 结构化数据
- [x] Step 2：可点击静态原型
- [x] Step 3：补期刊 2025–2026 范文与「怎么做的」拆解
- [ ] Step 4：真实图形摘要（模板图 / 文生图）
- [ ] Step 5：约束反查（非OA+几区 → 反推写法/癌种）
