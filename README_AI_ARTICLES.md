# AI Articles - GitHub Pages 部署说明

## 🌐 公开访问链接

**AI 文章页面：**
https://rebeccazpy-cloud.github.io/reply-collector/ai_articles.html

**原始文章页面：**
https://rebeccazpy-cloud.github.io/reply-collector/top_articles.html

---

## 📊 内容概览

### AI 文章筛选结果
- **扫描源数：** 92 个 RSS 源
- **找到的 AI 文章：** 63 篇
- **展示的精选文章：** 20 篇
- **质量分数范围：** 63-71

### AI 关键词过滤
包括但不限于：
- AI, Artificial Intelligence, Machine Learning, ML
- LLM, GPT, ChatGPT, Claude, Gemini
- Agentic Coding, Agent, Neural Network
- Deep Learning, NLP, Computer Vision
- Transformer, Embedding, Fine-tuning
- 等 40+ AI 相关术语

---

## 🔄 更新内容

如果您想更新文章内容：

### 1. 重新抓取文章
```bash
cd "/Volumes/T7 Shield/reply-collector"
python3 fetch_ai_articles.py
```

### 2. 提交到 Git
```bash
git add ai_articles.json
git commit -m "Update AI articles - $(date '+%Y-%m-%d')"
git push origin main
```

### 3. 等待部署
GitHub Pages 会自动部署，通常需要 1-2 分钟。

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `ai_articles.html` | AI 文章展示页面 |
| `ai_articles.json` | AI 文章数据（JSON 格式） |
| `fetch_ai_articles.py` | AI 文章抓取脚本 |
| `top_articles.html` | 所有高质量文章展示页面 |
| `top_articles.json` | 所有文章数据 |
| `fetch_articles.py` | 通用文章抓取脚本 |

---

## 🎨 页面特性

- ✅ 响应式设计，支持手机/平板/电脑
- ✅ 渐变紫蓝色背景
- ✅ 绿色 "AI" 徽章标识
- ✅ 质量评分系统
- ✅ 作者、日期、来源信息
- ✅ 可点击的文章链接

---

## 📤 分享方式

直接发送以下链接给他人：

```
https://rebeccazpy-cloud.github.io/reply-collector/ai_articles.html
```

任何人都可以通过浏览器访问，无需登录或权限。

---

## 🛠️ 技术栈

- **前端：** HTML5, CSS3, JavaScript
- **数据：** JSON
- **托管：** GitHub Pages
- **RSS 解析：** Python + feedparser
- **并发抓取：** ThreadPoolExecutor

---

**最后更新：** 2026-02-06
