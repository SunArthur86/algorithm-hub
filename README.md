# 🧮 算法面试题库 (Algorithm Interview)

> LeetCode 热题 100 **完整题解 + 逐题动画** + **热题 100 学习计划** + **三本书知识专栏** + **智能间隔复习**

🔗 **在线访问**: https://sunarthur86.github.io/algorithm-interview/

## ✨ 功能

### 📋 100 题完整题解（严格对齐热题 100）
- **完全复刻** [leetcode.cn/studyplan/top-100-liked](https://leetcode.cn/studyplan/top-100-liked/) 的 17 大分类
- **Java 为主要语言**，每题含解题思路、多解法、复杂度、关键点、陷阱（由 `public/legacy/sol-v2-*.js` 驱动）
- **100 题逐题动画**：统一 viz-engine.js Canvas 渲染器，7 种可视化类型（数组/链表/树/DP/矩阵/哈希/栈）
- **13 幅内联 SVG 图解**（静态）

### 📋 热题 100 学习计划
- 复刻力扣学习计划：大进度环、连续学习天数、预计完成日期
- 17 分类分组列表，勾选进度本地保存（localStorage）
- 勾选联动题库首页题卡

### 📚 算法知识专栏（三本书）
解析三本经典算法书籍为知识长文（共 174 篇）：
- 📘 **数据结构与算法之美**（极客时间，73 篇）
- 📗 **动态规划面试宝典**（20 篇）
- 📕 **labuladong 算法小抄**（Fucking-Algorithm，81 篇 + 342 幅图）

### 🔁 智能间隔复习
- **三种算法**：SM-2 智能间隔 / Leitner 卡盒 / 艾宾浩斯曲线
- 到期队列、四档评分（再来/困难/良好/简单）、下次复习时间预览
- 费曼快学卡 + 第一性原理卡（题目 frontmatter 驱动）

### 🎮 其他
- 收藏、自评掌握度、笔记
- 分类筛选 / 难度筛选 / 排序 / 搜索（带历史）
- 深色模式、PWA 离线、响应式

## 🛠 技术栈
- **Next.js 15**（App Router，`output: export` 静态导出 → GitHub Pages）
- **TypeScript** + **Tailwind CSS**
- gray-matter（markdown frontmatter）、react-markdown + remark-gfm + rehype-highlight
- zustand（状态持久化）
- Python 3 + BeautifulSoup4（epub）+ PyMuPDF（pdf）书籍解析

## 📂 项目结构
```
├── src/
│   ├── app/                # App Router 路由
│   │   ├── page.tsx        # 首页（题库）
│   │   ├── question/[lcId]/# 题目详情（SSG 100 页）
│   │   ├── study-plan/     # 热题100计划页
│   │   └── columns/        # 专栏目录 + [slug] 详情
│   ├── components/         # React 组件
│   └── lib/                # types/config/loaders/algorithms/store
├── questions/              # 100 题 markdown（17 分类）
├── columns/                # 三本书专栏 markdown（174 篇）
├── study-plan/             # top-100-liked.json
├── public/
│   ├── legacy/             # 旧项目可执行资产（viz-engine/轨迹/题解/SVG）
│   ├── columns/            # 专栏图片
│   ├── manifest.json       # PWA
│   └── sw.js               # Service Worker
├── legacy/                 # 旧 HTML/JS 项目备份
└── scripts/                # 数据迁移 + 书籍提取脚本
    ├── migrate_problems.py        # 100 题 → markdown
    ├── _epub_common.py            # epub 解析共享模块
    ├── extract_ds_beauty.py       # 数据结构与算法之美
    ├── extract_dp_book.py         # 动态规划面试宝典
    └── extract_labuladong.py      # labuladong PDF
```

## 🚀 开发与部署

```bash
npm install      # 安装依赖
npm run dev      # 本地开发 (http://localhost:3000)
npm run build    # 静态导出到 out/
```

### 重新生成数据

```bash
# 100 题从 legacy 数据迁移为 markdown
python3 scripts/migrate_problems.py

# 三本书解析为专栏（需 pip install beautifulsoup4 PyMuPDF）
python3 scripts/extract_ds_beauty.py
python3 scripts/extract_dp_book.py
python3 scripts/extract_labuladong.py
```

### 部署到 GitHub Pages
`next.config.ts` 已配置 `output: 'export'` + `basePath: '/algorithm-interview'`。
`npm run build` 后将 `out/` 发布到 gh-pages 分支即可。

## ⌨ 快捷键
| 快捷键 | 功能 |
|--------|------|
| `←` `→` | 上一题 / 下一题（弹窗内） |
| `Esc` | 关闭弹窗 |

## 📊 数据统计
- **100 题**（热题 100，17 分类）
- **174 篇专栏**（3 本书）
- **100 题逐题动画** + 18 种算法动画 + 13 幅 SVG 图解
- **280 个静态页面**

## ⚠️ 备注
- 旧版纯 HTML/JS 项目保留在 `legacy/`，动画引擎等可执行资产复制到 `public/legacy/` 供客户端组件复用。
- 题目 frontmatter 的 `feynman`/`first_principle` 字段由题解 thinking 推导生成，可逐题人工补全。

📅 2026 · Next.js 重构版
