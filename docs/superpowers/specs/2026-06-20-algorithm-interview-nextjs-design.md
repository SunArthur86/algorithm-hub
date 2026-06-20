# algorithm-interview Next.js 重构设计

> 日期：2026-06-20
> 状态：待用户最终确认
> 目标项目：`/Users/sunqingguang/hermes/opt/projects/algorithm-interview`

## 1. 背景与目标

当前 `algorithm-interview` 是纯 HTML + CSS + JavaScript 项目，已包含：

- 100 道 LeetCode 热题 100（`js/problems-data.js`，严格对齐 leetcode 17 大分类）
- 100 题完整 Java 题解（`js/sol-v2-*.js`，13 个批次）
- 100 题逐题 Canvas 动画轨迹（`js/viz-traces-*.js`，6 个文件）
- 18 种算法动画 + 13 幅内联 SVG 图解
- PWA 离线支持

参考项目 `ai-interview/` 与 `java-interview/` 已迁移到 Next.js 15 + TypeScript + Tailwind（App Router），具备 markdown frontmatter 题库、费曼快学、第一性原理、SM-2/Leitner/艾宾浩斯三种智能复习算法。

本设计将 algorithm-interview **重构为 Next.js**，并完成三项工作：

1. **Next.js 重构**：架构对齐 java-interview，全量复刻其高级能力（费曼/第一性原理/复习），并保留所有原有算法动画资产。
2. **学习计划**：新增「LeetCode 热题 100」学习计划，复刻 leetcode.cn/studyplan/top-100-liked 的进度追踪体验。
3. **知识专栏**：解析 `/Users/sunqingguang/Downloads/02.interview/算法` 下三本书，转为算法知识专栏。

## 2. 已确认决策

| 决策点 | 选择 |
|--------|------|
| 三本书的内容形态 | **算法知识专栏**（独立板块，与 100 题并列的长文） |
| 学习计划复杂度 | **仅热题 100 计划**（不做自定义计划/每日量配置） |
| 重构范围 | **全量复刻**（Next.js 架构 + 所有算法资产 + 费曼/第一性原理/复习功能） |
| 重构位置 | **原仓库内重构**（旧文件移 `legacy/`，git 历史保留） |

## 3. 架构方案选型

对比三种方案：

- **方案 A（推荐）：渐进式迁移**。旧 `index.html/js/css` 整体移入 `legacy/`，根目录初始化 Next.js；100 题文本转 markdown；动画引擎（`viz-engine.js`/`diagrams.js`/`algorithm-visualizer.js`）与轨迹数据原样保留为 `public/legacy/`，用客户端组件复用，**不重写动画引擎**。
- **方案 B：纯 React 重写**。动画也用 React/Canvas 重写。代价：100 题轨迹 + 18 算法动画重写工作量巨大，回归风险高。
- **方案 C：iframe 套壳**。旧页 iframe 嵌入。违反"全量复刻"意图，体验割裂。

**采用方案 A**：零风险保留最贵的动画资产，同时获得 java-interview 全部高级功能。

## 4. 数据模型

### 4.1 目录结构

```
algorithm-interview/
├── legacy/                      # 旧项目备份（git 历史保留）
│   ├── index.html
│   ├── js/ (problems-data.js, sol-v2-*.js, viz-traces-*.js, viz-engine.js, ...)
│   └── css/
├── public/
│   └── legacy/                  # 客户端可执行资产（动画引擎 + 轨迹 + SVG）
│       ├── viz-engine.js
│       ├── viz-traces-*.js
│       ├── algorithm-visualizer.js
│       ├── visualizer-extended.js
│       ├── diagrams.js
│       └── sol-v2-*.js          # 题解（按 lcId 索引）
├── questions/                   # 100 题 markdown（按热题100的17分类）
│   ├── hash/
│   │   ├── 0001-two-sum.md
│   │   └── 0049-group-anagrams.md
│   ├── two-pointers/
│   └── ...
├── columns/                     # 知识专栏（书的内容，长文）
│   ├── data-structure-beauty/
│   ├── dynamic-programming/
│   └── labuladong/
├── study-plan/
│   └── top-100-liked.json
├── scripts/                     # 提取/迁移脚本（Python）
└── src/                         # Next.js 源码
```

### 4.2 题目 frontmatter

兼容 java-interview 字段并增加算法专属字段：

```yaml
---
id: "0001"                       # 4位补零，便于排序
slug: "two-sum"
lcId: 1                          # 力扣题号（索引 legacy 动画/题解）
title: "两数之和"
difficulty: "Easy"               # Easy/Medium/Hard
category: "hash"                 # 热题100分类
tags: ["数组", "哈希表"]
url: "https://leetcode.cn/problems/two-sum/"
planOrder: 1                     # 在热题100中的顺序号 1-100
hasViz: true                     # 是否有逐题动画
hasDiagram: true                 # 是否有 SVG 图解
feynman:
  essence: "..."
  analogy: "..."
  key_points: ["..."]
first_principle:
  problem: "..."
  axioms: ["..."]
  rebuild: "..."
---

# 两数之和

题目描述 + 示例...

## 题解

解题思路、多解法、复杂度、陷阱...
```

**约定**：`SOLUTIONS`/`VIZ_TRACES`/`diagrams` 是可执行动画代码而非纯文本，**不从 markdown 读取**，作为客户端 JS 资产留在 `public/legacy/`，按 `lcId` 索引。markdown 只存文本与 frontmatter 元数据。

### 4.3 专栏 frontmatter

```yaml
---
slug: sliding-window-template
title: "滑动窗口算法核心模板"
source: labuladong                # data-structure-beauty / dynamic-programming / labuladong
chapter: "滑动窗口技巧"
order: 3
related: [3, 438, 76]             # 关联的热题100 lcId（交叉跳转）
---

正文 markdown，保留原书小标题、代码块、图...
```

## 5. UI 与路由

```
src/app/
├── layout.tsx                  # 根布局：全局 CSS、深色模式、PWA manifest
├── page.tsx                    # 首页（Server）→ <HomeClient/>
├── globals.css                 # Tailwind + CSS 变量
├── question/[lcId]/page.tsx    # 题目详情（generateStaticParams 100 题）
├── study-plan/page.tsx         # 热题100计划页
├── columns/page.tsx            # 专栏目录
└── columns/[slug]/page.tsx     # 专栏详情
```

```
src/components/
├── HomeClient.tsx              # 首页主壳：分类Tab + 卡片网格
├── CategoryTabs.tsx            # 17 分类（哈希/双指针/.../技巧）
├── QuestionCard.tsx            # 题目卡（题号、标题、难度、完成✓、收藏★、有动画🎬）
├── FilterBar.tsx / SearchBar.tsx / DifficultyBars.tsx
├── QuestionModal.tsx           # 题目弹窗（题解 + 动画 + 费曼 + 第一性原理）
├── VizPlayer.tsx               # 客户端组件：挂载 legacy viz-engine + 按 lcId 取轨迹
├── StudyPlan.tsx               # 热题100计划组件（进度环 + 勾选列表）
├── FeynmanCard.tsx / FirstPrincipleCard.tsx
├── ReviewDashboard.tsx / ReviewMode.tsx
├── ProgressRing.tsx / Toast.tsx / Markdown.tsx
└── SettingsPanel.tsx
```

**交互约定**：题目详情支持弹窗/路由双模式（列表点开弹窗，`/question/[lcId]` 为永久链接）。动画播放器用 `dynamic(import, { ssr:false })` 避免 SSR `window` 报错。

## 6. 知识专栏生成（书 → columns/）

三个 Python 提取脚本（放 `scripts/`，沿用 java-interview `extract_book.py` 模式）：

| 脚本 | 输入 | 产出 |
|------|------|------|
| `extract_ds_beauty.py` | `01-数据结构与算法之美.epub` | `columns/data-structure-beauty/*.md`（按章节） |
| `extract_dp_book.py` | `156-动态规划面试宝典.epub` | `columns/dynamic-programming/*.md` |
| `extract_labuladong.py` | `Fucking-Algorithm.pdf` | `columns/labuladong/*.md` |

**流程**：
- epub → 解压 XHTML → BeautifulSoup 抽正文 → 去水印/版权页 → 按章拆 → 写 md
- PDF → PyMuPDF(fitz) 抽目录 + 正文 → 图文保留（图存 `public/columns/<source>/`）

每个脚本可独立重跑，含去重清洗（参考 java-interview `r4r5r9_quality.py`）。专栏正文中的图引用相对路径。

## 7. 学习计划（复刻热题 100）

`study-plan/top-100-liked.json`，数据来自现有 `problems-data.js` 顺序（已严格对齐 leetcode 17 分类）：

```json
{
  "slug": "top-100-liked",
  "title": "LeetCode 热题 100",
  "groups": [
    { "name": "哈希", "problems": ["1","49","128"] },
    { "name": "双指针", "problems": ["283","11","15","42"] }
  ]
}
```

**StudyPlan 页面复刻 leetcode 学习计划**：
- 顶部大进度环（X/100 完成）+ 连续学习 N 天 + 预计完成日期
- 17 分类分组列表，每题一行：勾选框 + 题号 + 标题 + 难度色条 + 跳转
- 勾选状态存 localStorage（key=`algo-interview:plan-progress`），勾选联动题库首页题卡✓
- 不做自定义计划/每日量配置

## 8. 复习系统（复刻 java-interview）

直接移植 java-interview 三件套，零改动逻辑：

- **三种算法**（`src/lib/algorithms.ts`）：SM-2 智能间隔 / Leitner 卡盒 / 艾宾浩斯曲线，SettingsPanel 可切换
- **复习数据**：每题记 `nextReview / interval / ease / reps / lapses`，存 localStorage
- **ReviewDashboard**：到期题排队，复习完打分（再来/困难/良好/简单）更新间隔
- **费曼卡 + 第一性原理卡**：题目 frontmatter 的 `feynman`/`first_principle` 驱动

## 9. 技术栈

Next.js 15（App Router，`next.config.ts` 用 `output:'export'` 静态导出 → GitHub Pages）+ TypeScript + Tailwind + gray-matter + remark/rehype-highlight。

## 10. 里程碑

1. 初始化 Next.js 骨架，legacy 备份，迁移 100 题为 markdown（脚本）
2. 首页 + 题目详情 + 弹窗（接入 legacy 动画/题解资产）
3. 热题100计划页
4. 三本书提取脚本 + 专栏页
5. 复习系统（SM-2/Leitner/费曼/第一性原理）移植
6. PWA + 深色模式 + 部署校验

## 11. 风险与备注

- **动画资产互操作**：legacy JS 通过 `window.VIZ_TRACES`/`window.SOLUTIONS` 全局暴露，客户端组件按 lcId 取用；需在 VizPlayer 挂载时确保脚本加载顺序。
- **PDF 体量大**：labuladong PDF ~100MB，提取脚本需流式处理，图片按需导出。
- **frontmatter 完整性**：迁移脚本需为每题生成 `feynman`/`first_principle`（可由题解 thinking/approaches 推导，缺失项留待人工补充）。
- **静态导出兼容**：所有页面须可静态预渲染；localStorage 仅在客户端组件使用。
