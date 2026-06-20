---
id: "0128"
slug: "longest-consecutive-sequence"
lcId: 128
title: "最长连续序列"
difficulty: "Medium"
category: "hash"
tags:
  - "并查集"
  - "数组"
  - "哈希表"
url: "https://leetcode.cn/problems/longest-consecutive-sequence/"
planOrder: 3
hasViz: true
hasDiagram: false
feynman:
  essence: "找最长的连续整数序列。暴力排序后遍历是 O(n log n)，但可以做到 O(n)。关键观察：从序列的起点（即 num-1 不在集合中）开始向后数，每个元素最多"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 128. 最长连续序列

> 难度：Medium | 分类：哈希 | 标签：并查集, 数组, 哈希表
> 力扣链接：[https://leetcode.cn/problems/longest-consecutive-sequence/](https://leetcode.cn/problems/longest-consecutive-sequence/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

找最长的连续整数序列。暴力排序后遍历是 O(n log n)，但可以做到 O(n)。关键观察：从序列的起点（即 num-1 不在集合中）开始向后数，每个元素最多被访问两次。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
