# 部署到 Render（在线访问）

目标链接形态：`https://你起的名字.onrender.com`

## 前提

Render 的 Static Site **必须连 Git 仓库**（GitHub / GitLab / Bitbucket）。本机 `localhost` 无法被别人直接打开。

## 推荐做法：只把 `website/` 推成一个小仓库

### 1. 新建 GitHub 空仓库

例如仓库名：`multi-cancer-desk`

### 2. 在本机初始化并推送（只推 website）

在 PowerShell 里：

```powershell
cd "d:\hyf\freelance-work\niumayuan\2026\公开组学选题助手\website"

git init
git add index.html assets data render.yaml README.md serve.py
git commit -m "Deploy decision desk static site"
git branch -M main
git remote add origin https://github.com/你的用户名/multi-cancer-desk.git
git push -u origin main
```

> 若还没登录 GitHub CLI：先跑 `gh auth login`，或在网页上手动 New repository。

### 3. 在 Render 创建 Static Site

1. 打开 [https://dashboard.render.com/](https://dashboard.render.com/)
2. **New → Static Site**
3. 连接刚才的 GitHub 仓库
4. 填写：
   - **Name**：`multi-cancer-desk`（可改）
   - **Branch**：`main`
   - **Build Command**：留空
   - **Publish Directory**：`.`（一个点）
5. 点 **Create Static Site**

等一两分钟，顶部会出现公网地址，例如：

`https://multi-cancer-desk.onrender.com`

把这个链接发给别人即可在线访问。

### 4. 以后改内容怎么更新

改完本地文件后：

```powershell
cd website
git add -A
git commit -m "Update content"
git push
```

Render 会自动重新部署。

---

## 若整仓推送「公开组学选题助手」根目录

Publish Directory 改成：`website`  
（不要写成 `website/` 以外的路径；Build Command 仍留空。）

---

## 常见问题

| 现象 | 处理 |
|------|------|
| 页面空白 / JSON 404 | Publish Directory 必须指向含 `index.html` 和 `data/` 的目录 |
| Free 实例睡醒慢 | 静态站一般很快；若连的是 Web Service 才有冷启动 |
| 想自定义域名 | Render → Settings → Custom Domains |
