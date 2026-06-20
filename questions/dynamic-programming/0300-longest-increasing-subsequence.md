---
id: "0300"
slug: "longest-increasing-subsequence"
lcId: 300
title: "最长递增子序列"
difficulty: "Medium"
category: "dynamic-programming"
tags:
  - "数组"
  - "二分查找"
  - "动态规划"
url: "https://leetcode.cn/problems/longest-increasing-subsequence/"
planOrder: 87
hasViz: true
hasDiagram: false
feynman:
  essence: "给你一个整数数组 `nums`，找到最长严格递增子序列的长度。子序列不要求连续，但要求保持原始顺序。  重点不在\"怎么枚举所有子序列\"，而在\"怎么用 DP 或二分高效地找到最长长度\"。"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 300. 最长递增子序列

> 难度：**Medium** | 分类：动态规划 | 标签：数组, 二分查找, 动态规划

> 🔗 力扣链接：[https://leetcode.cn/problems/longest-increasing-subsequence/](https://leetcode.cn/problems/longest-increasing-subsequence/)

## 📝 题目描述

给你一个整数数组 `nums`，找到最长严格递增子序列的长度。子序列不要求连续，但要求保持原始顺序。

重点不在"怎么枚举所有子序列"，而在"怎么用 DP 或二分高效地找到最长长度"。

- 题号：300
- 题目名：最长递增子序列
- 难度：中等
- 题型：动态规划
- 为什么选这题：它是 DP 的经典中的经典，O(n²) 的 DP 解法和 O(n log n) 的二分优化都值得掌握。

## 🧠 思考路径

**方法一：O(n²) DP**

设 `dp[i]` 表示以 `nums[i]` 结尾的最长递增子序列的长度。对于每个 `i`，检查所有 `j < i`：如果 `nums[j] < nums[i]`，则 `dp[i] = max(dp[i], dp[j] + 1)`。最终答案是 `max(dp[i])`。

**方法二：O(n log n) 贪心 + 二分**

维护一个数组 `tails`，`tails[i]` 表示长度为 `i+1` 的递增子序列的最小末尾元素。遍历 `nums`，对每个元素在 `tails` 中二分查找：
- 如果比所有 `tails` 都大，追加到末尾（递增子序列变长了）。
- 否则，替换第一个 ≥ 它的元素（让末尾尽可能小，给后续元素更多空间）。

`tails` 的长度就是答案。

所以这题的关键词不是"枚举子序列"，而是"DP 看前面比它小的 +1"或"贪心地维护最小末尾 + 二分"。

## 💻 Java 题解

### 解法 1：动态规划 O(n²)

dp[i]=max(dp[j]+1) for all j<i and nums[j]<nums[i]。

- ⏱ 时间复杂度：`O(n²)`
- 💾 空间复杂度：`O(n)`

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] dp = new int[nums.length];
        Arrays.fill(dp, 1);
        int maxLen = 1;
        for (int i = 1; i < nums.length; i++) {
            for (int j = 0; j < i; j++)
                if (nums[j] < nums[i]) dp[i] = Math.max(dp[i], dp[j] + 1);
            maxLen = Math.max(maxLen, dp[i]);
        }
        return maxLen;
    }
}
```

**关键点：**
- dp[i]=以i结尾的最长LIS
- 双重循环
- 取全局最大值

**执行步骤：**
1. 初始化dp全1
1. 枚举j<i
1. nums[j]<nums[i]时更新dp[i]
1. 返回max


### 解法 2：二分查找 O(n log n)

维护一个递增数组tails，对每个nums[i]二分找位置替换。

- ⏱ 时间复杂度：`O(n log n)`
- 💾 空间复杂度：`O(n)`

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;
        for (int num : nums) {
            int lo = 0, hi = size;
            while (lo < hi) {
                int mid = (lo + hi) / 2;
                if (tails[mid] < num) lo = mid + 1;
                else hi = mid;
            }
            tails[lo] = num;
            if (lo == size) size++;
        }
        return size;
    }
}
```

**关键点：**
- tails数组始终有序
- 二分找第一个>=num的位置
- lo==size 时数组扩展

**执行步骤：**
1. 对每个num二分
1. 替换或扩展tails
1. 返回size


## ⚠️ 易错点

- 二分查找用 `bisect_left`（找第一个 ≥ 的位置），不是 `bisect_right`。
- `tails` 数组并不代表实际的 LIS，只是长度正确。
- 严格递增：`nums[j] < nums[i]`，不是 `<=`。

- dp法是'以i结尾'不是'前i个'

- 二分法找的是第一个>=num的位置

## 📊 复杂度分析

- 时间复杂度：`O(n log n)`（二分优化）或 `O(n²)`（DP）。
- 空间复杂度：`O(n)`。

## 🏢 实际业务应用

- 推荐系统中，找出用户兴趣变化的趋势（最长递增序列）。
- 股票分析中，找出最长连续上涨的天数（子序列版本）。
- 版本管理中，找出最长的不冲突的提交序列。
- 生物信息学中，RNA 二级结构预测中用到 LIS。

- 推荐系统中，找出用户兴趣变化的趋势（最长递增序列）。
- 股票分析中，找出最长连续上涨的天数（子序列版本）。
- 版本管理中，找出最长的不冲突的提交序列。
- 生物信息学中，RNA 二级结构预测中用到 LIS。

## 📖 形象类比

可以把它类比成《水浒传》里梁山泊按武力值找最长"递增"的师徒链。

一百零八将按入伙顺序排列，宋江想找一串好汉，使得后入伙的每一个都比前面那个武力值更高（但不用连续入伙）。他用两种方法：简单的方法是看每个人之前有多少比他弱的好汉（O(n²) DP）；聪明的方法是维护一个列表，只记录"每个长度下最弱的末位好汉"，用二分快速查找（O(n log n)）。

对应关系是：

- "数组"对应按入伙顺序的好汉列表
- "严格递增"对应后入伙的更强
- "tails"对应"每个长度下最弱的末位好汉"
- "二分替换"对应用更弱的好汉替换，给后面留更多空间

这段记忆的关键是：tails 数组只关心"能不能让序列更长"，不关心具体是哪些元素。

可以把它类比成《水浒传》里梁山泊按武力值找最长"递增"的师徒链。

一百零八将按入伙顺序排列，宋江想找一串好汉，使得后入伙的每一个都比前面那个武力值更高（但不用连续入伙）。他用两种方法：简单的方法是看每个人之前有多少比他弱的好汉（O(n²) DP）；聪明的方法是维护一个列表，只记录"每个长度下最弱的末位好汉"，用二分快速查找（O(n log n)）。

对应关系是：

- "数组"对应按入伙顺序的好汉列表
- "严格递增"对应后入伙的更强
- "tails"对应"每个长度下最弱的末位好汉"
- "二分替换"对应用更弱的好汉替换，给后面留更多空间

这段记忆的关键是：tails 数组只关心"能不能让序列更长"，不关心具体是哪些元素。

小松鼠收集了一串松果，按找到的顺序排列。它想知道最长一串"越来越重"的松果子序列有多长。它维护一个小本子，记下"长度为 k 的子序列中最轻的末尾松果是哪颗"。每来一颗新松果，就用二分法在本子里找位置，让末尾尽可能小。

小松鼠收集了一串松果，按找到的顺序排列。它想知道最长一串"越来越重"的松果子序列有多长。它维护一个小本子，记下"长度为 k 的子序列中最轻的末尾松果是哪颗"。每来一颗新松果，就用二分法在本子里找位置，让末尾尽可能小。

## 🎵 记忆口诀

DP 看前比小加一，二分维护最小末尾。

DP 看前比小加一，二分维护最小末尾。

## 🔗 延伸练习

- `354. 俄罗斯套娃信封问题`：二维版本的 LIS，先排序再套用本题。
- `673. 最长递增子序列的个数`：不仅求长度，还要求有多少条。

- `354. 俄罗斯套娃信封问题`：二维版本的 LIS，先排序再套用本题。
- `673. 最长递增子序列的个数`：不仅求长度，还要求有多少条。
