---
id: "0049"
slug: "group-anagrams"
lcId: 49
title: "字母异位词分组"
difficulty: "Medium"
category: "hash"
tags:
  - "数组"
  - "哈希表"
  - "字符串"
url: "https://leetcode.cn/problems/group-anagrams/"
planOrder: 2
hasViz: true
hasDiagram: false
feynman:
  essence: "字母异位词是指字母相同但排列不同的字符串。如果把每个字符串的字符排序，那么所有互为异位词的字符串排序后结果相同。因此可以用排序后的字符串作为哈希键来分组。另一种"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 49. 字母异位词分组

> 难度：Medium | 分类：哈希 | 标签：数组, 哈希表, 字符串
> 力扣链接：[https://leetcode.cn/problems/group-anagrams/](https://leetcode.cn/problems/group-anagrams/)

## 题目描述

（待从力扣补充题目描述与示例）

## 题解

字母异位词是指字母相同但排列不同的字符串。如果把每个字符串的字符排序，那么所有互为异位词的字符串排序后结果相同。因此可以用排序后的字符串作为哈希键来分组。另一种方法是统计每个字母的出现次数作为键。

> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。
