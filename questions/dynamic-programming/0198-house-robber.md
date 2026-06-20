---
id: "0198"
slug: "house-robber"
lcId: 198
title: "打家劫舍"
difficulty: "Medium"
category: "dynamic-programming"
tags:
  - "数组"
  - "动态规划"
url: "https://leetcode.cn/problems/house-robber/"
planOrder: 83
hasViz: true
hasDiagram: false
feynman:
  essence: "打家劫舍。不能偷相邻的。dp[i]=max(dp[i-1], dp[i-2]+nums[i])。"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 198. 打家劫舍

> 难度：Medium | 分类：动态规划 | 标签：数组, 动态规划
> 力扣链接：[https://leetcode.cn/problems/house-robber/](https://leetcode.cn/problems/house-robber/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

打家劫舍。不能偷相邻的。dp[i]=max(dp[i-1], dp[i-2]+nums[i])。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
