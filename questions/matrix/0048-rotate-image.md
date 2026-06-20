---
id: "0048"
slug: "rotate-image"
lcId: 48
title: "旋转图像"
difficulty: "Medium"
category: "matrix"
tags:
  - "数组"
  - "数学"
  - "矩阵"
url: "https://leetcode.cn/problems/rotate-image/"
planOrder: 20
hasViz: true
hasDiagram: false
feynman:
  essence: "顺时针旋转图像 90°。先转置（沿主对角线翻转），再水平翻转每行。或者直接找旋转规律：matrix[i][j]→matrix[j][n-1-i]。"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 48. 旋转图像

> 难度：Medium | 分类：矩阵 | 标签：数组, 数学, 矩阵
> 力扣链接：[https://leetcode.cn/problems/rotate-image/](https://leetcode.cn/problems/rotate-image/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

顺时针旋转图像 90°。先转置（沿主对角线翻转），再水平翻转每行。或者直接找旋转规律：matrix[i][j]→matrix[j][n-1-i]。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
