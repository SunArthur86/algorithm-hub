---
id: "0560"
slug: "subarray-sum-equals-k"
lcId: 560
title: "和为 K 的子数组"
difficulty: "Medium"
category: "substring"
tags:
  - "数组"
  - "哈希表"
  - "前缀和"
url: "https://leetcode.cn/problems/subarray-sum-equals-k/"
planOrder: 10
hasViz: true
hasDiagram: false
feynman:
  essence: "求和为 k 的子数组个数。暴力 O(n²)，但可以用前缀和+哈希表优化到 O(n)。核心：prefix[j]-prefix[i]=k 等价于找之前有多少个前缀和"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 560. 和为 K 的子数组

> 难度：Medium | 分类：子串 | 标签：数组, 哈希表, 前缀和
> 力扣链接：[https://leetcode.cn/problems/subarray-sum-equals-k/](https://leetcode.cn/problems/subarray-sum-equals-k/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

求和为 k 的子数组个数。暴力 O(n²)，但可以用前缀和+哈希表优化到 O(n)。核心：prefix[j]-prefix[i]=k 等价于找之前有多少个前缀和等于 prefix[j]-k。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
