---
id: "0011"
slug: "container-with-most-water"
lcId: 11
title: "盛最多水的容器"
difficulty: "Medium"
category: "two-pointers"
tags:
  - "贪心"
  - "数组"
  - "双指针"
url: "https://leetcode.cn/problems/container-with-most-water/"
planOrder: 5
hasViz: true
hasDiagram: false
feynman:
  essence: "两条线段和 x 轴围成的容器，水量 = min(h[i],h[j]) × (j-i)。要最大化水量。双指针从两端出发，每次移动较短的一边——因为移动较长的一边不"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 11. 盛最多水的容器

> 难度：Medium | 分类：双指针 | 标签：贪心, 数组, 双指针
> 力扣链接：[https://leetcode.cn/problems/container-with-most-water/](https://leetcode.cn/problems/container-with-most-water/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

两条线段和 x 轴围成的容器，水量 = min(h[i],h[j]) × (j-i)。要最大化水量。双指针从两端出发，每次移动较短的一边——因为移动较长的一边不可能让水量增加。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
