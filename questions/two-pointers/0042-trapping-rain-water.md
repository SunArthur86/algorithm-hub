---
id: "0042"
slug: "trapping-rain-water"
lcId: 42
title: "接雨水"
difficulty: "Hard"
category: "two-pointers"
tags:
  - "栈"
  - "数组"
  - "双指针"
  - "动态规划"
url: "https://leetcode.cn/problems/trapping-rain-water/"
planOrder: 7
hasViz: true
hasDiagram: true
feynman:
  essence: "接雨水问题。每个位置能接的雨水量 = min(左侧最高, 右侧最高) - 当前高度。三种解法：动态规划预处理左右最大值、双指针、单调栈。"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 42. 接雨水

> 难度：Hard | 分类：双指针 | 标签：栈, 数组, 双指针, 动态规划
> 力扣链接：[https://leetcode.cn/problems/trapping-rain-water/](https://leetcode.cn/problems/trapping-rain-water/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

接雨水问题。每个位置能接的雨水量 = min(左侧最高, 右侧最高) - 当前高度。三种解法：动态规划预处理左右最大值、双指针、单调栈。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
