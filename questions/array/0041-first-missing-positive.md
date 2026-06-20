---
id: "0041"
slug: "first-missing-positive"
lcId: 41
title: "缺失的第一个正数"
difficulty: "Hard"
category: "array"
tags:
  - "数组"
  - "哈希表"
url: "https://leetcode.cn/problems/first-missing-positive/"
planOrder: 17
hasViz: true
hasDiagram: false
feynman:
  essence: "找缺失的第一个正数，要求 O(n) 时间 O(1) 空间。核心思路：把每个合法的正数放到它应该在的位置（nums[i] 放到 nums[nums[i]-1]），"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 41. 缺失的第一个正数

> 难度：Hard | 分类：普通数组 | 标签：数组, 哈希表
> 力扣链接：[https://leetcode.cn/problems/first-missing-positive/](https://leetcode.cn/problems/first-missing-positive/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

找缺失的第一个正数，要求 O(n) 时间 O(1) 空间。核心思路：把每个合法的正数放到它应该在的位置（nums[i] 放到 nums[nums[i]-1]），再扫描找第一个不匹配的。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
