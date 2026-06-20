---
id: "0001"
slug: "two-sum"
lcId: 1
title: "两数之和"
difficulty: "Easy"
category: "hash"
tags:
  - "数组"
  - "哈希表"
url: "https://leetcode.cn/problems/two-sum/"
planOrder: 1
hasViz: true
hasDiagram: true
feynman:
  essence: "给定数组和目标值，找两个数使其和等于目标。最直观的思路是双重循环暴力枚举，但时间复杂度 O(n²)。更优的方案是用哈希表——对每个元素 nums[i]，只需检查"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 1. 两数之和

> 难度：Easy | 分类：哈希 | 标签：数组, 哈希表
> 力扣链接：[https://leetcode.cn/problems/two-sum/](https://leetcode.cn/problems/two-sum/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

给定数组和目标值，找两个数使其和等于目标。最直观的思路是双重循环暴力枚举，但时间复杂度 O(n²)。更优的方案是用哈希表——对每个元素 nums[i]，只需检查 target - nums[i] 是否已经在哈希表中，这样只需一次遍历。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
