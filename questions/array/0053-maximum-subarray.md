---
id: "0053"
slug: "maximum-subarray"
lcId: 53
title: "最大子数组和"
difficulty: "Medium"
category: "array"
tags:
  - "数组"
  - "分治"
  - "动态规划"
url: "https://leetcode.cn/problems/maximum-subarray/"
planOrder: 13
hasViz: true
hasDiagram: true
feynman:
  essence: "最大子数组和。Kadane算法：dp[i]=max(nums[i], dp[i-1]+nums[i])。用单变量优化空间。"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 53. 最大子数组和

> 难度：Medium | 分类：普通数组 | 标签：数组, 分治, 动态规划
> 力扣链接：[https://leetcode.cn/problems/maximum-subarray/](https://leetcode.cn/problems/maximum-subarray/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

最大子数组和。Kadane算法：dp[i]=max(nums[i], dp[i-1]+nums[i])。用单变量优化空间。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
