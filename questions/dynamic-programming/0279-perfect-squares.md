---
id: "0279"
slug: "perfect-squares"
lcId: 279
title: "完全平方数"
difficulty: "Medium"
category: "dynamic-programming"
tags:
  - "广度优先搜索"
  - "数学"
  - "动态规划"
url: "https://leetcode.cn/problems/perfect-squares/"
planOrder: 84
hasViz: true
hasDiagram: false
feynman:
  essence: "完全平方数。dp[i]=min(dp[i-j²]+1) for all j²<=i。BFS也可以。"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 279. 完全平方数

> 难度：Medium | 分类：动态规划 | 标签：广度优先搜索, 数学, 动态规划
> 力扣链接：[https://leetcode.cn/problems/perfect-squares/](https://leetcode.cn/problems/perfect-squares/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

完全平方数。dp[i]=min(dp[i-j²]+1) for all j²<=i。BFS也可以。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
