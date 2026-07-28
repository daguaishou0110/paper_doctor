# 公开组学 · 选刊选题助手（网站）

静态站点：写法百科 → 期刊情报 → 癌种选题。

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
    ├── FIELD_DICTIONARY.md
    ├── meta.json
    ├── methods.json
    ├── journals.json
    ├── cancers.json
    ├── papers.json
    └── expand_website_from_progress.py
```
