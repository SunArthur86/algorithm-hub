---
id: "0064"
slug: "minimum-path-sum"
lcId: 64
title: "最小路径和"
difficulty: "Medium"
category: "multi-dp"
tags:
  - "数组"
  - "动态规划"
  - "矩阵"
url: "https://leetcode.cn/problems/minimum-path-sum/"
planOrder: 92
hasViz: true
hasDiagram: false
feynman:
  essence: "最小路径和。dp[i][j]=grid[i][j]+min(dp[i-1][j], dp[i][j-1])。"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 64. 最小路径和

> 难度：Medium | 分类：多维动态规划 | 标签：数组, 动态规划, 矩阵
> 力扣链接：[https://leetcode.cn/problems/minimum-path-sum/](https://leetcode.cn/problems/minimum-path-sum/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

最小路径和。dp[i][j]=grid[i][j]+min(dp[i-1][j], dp[i][j-1])。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
