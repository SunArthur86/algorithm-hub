---
id: "0034"
slug: "find-first-and-last-position-of-element-in-sorted-array"
lcId: 34
title: "在排序数组中查找元素的第一个和最后一个位置"
difficulty: "Medium"
category: "binary-search"
tags:
  - "数组"
  - "二分查找"
url: "https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/"
planOrder: 65
hasViz: true
hasDiagram: false
feynman:
  essence: "给你一个非递减排序的整数数组和一个目标值 `target`，返回 `target` 在数组中第一次和最后一次出现的下标。如果 `target` 不存在，返回 `[-1, -1]`。  要求时间复杂度"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 34. 在排序数组中查找元素的第一个和最后一个位置

> 难度：**Medium** | 分类：二分查找 | 标签：数组, 二分查找

> 🔗 力扣链接：[https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)

## 📝 题目描述

给你一个非递减排序的整数数组和一个目标值 `target`，返回 `target` 在数组中第一次和最后一次出现的下标。如果 `target` 不存在，返回 `[-1, -1]`。

要求时间复杂度 `O(log n)`。

- 题号：34
- 题目名：在排序数组中查找元素的第一个和最后一个位置
- 难度：中等
- 题型：二分查找
- 为什么选这题：它把"二分查找"从"找一个点"拓展到"找左右边界"，是理解二分查找变体的核心题。

## 🧠 思考路径

普通的二分找到 `target` 就停了，但这里有重复元素，我们需要找到最左和最右的位置。

换一个角度看：找"第一个位置"等价于找"第一个大于等于 `target` 的位置"，然后再验证这个位置是不是真的是 `target`。找"最后一个位置"等价于找"最后一个小于等于 `target` 的位置"。

具体来说，写两个二分：一个找左边界，一个找右边界。

找左边界时，当 `nums[mid] == target` 不要立刻返回，而是让 `right = mid - 1` 继续往左压，最终 `left` 会停在最左边那个 `target` 上。

找右边界时，当 `nums[mid] == target` 不要立刻返回，而是让 `left = mid + 1` 继续往右压，最终 `right` 会停在最右边那个 `target` 上。

两个二分跑完，验证一下 `left` 和 `right` 位置上的值是否真的是 `target` 即可。

## 💻 Java 题解

### 解法 1：两次二分

第一次二分找左边界（找到target后继续向左），第二次找右边界（找到target后继续向右）。

- ⏱ 时间复杂度：`O(log n)`
- 💾 空间复杂度：`O(1)`

```java
class Solution {
    public int[] searchRange(int[] nums, int target) {
        int left = findLeft(nums, target);
        int right = findRight(nums, target);
        return new int[]{left, right};
    }
    private int findLeft(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1, idx = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] >= target) hi = mid - 1;
            else lo = mid + 1;
            if (nums[mid] == target) idx = mid;
        }
        return idx;
    }
    private int findRight(int[] nums, int target) {
        int lo = 0, hi = nums.length - 1, idx = -1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] <= target) lo = mid + 1;
            else hi = mid - 1;
            if (nums[mid] == target) idx = mid;
        }
        return idx;
    }
}
```

**关键点：**
- findLeft: nums[mid]>=target 时hi=mid-1
- findRight: nums[mid]<=target 时lo=mid+1
- 记录最后的匹配位置

**执行步骤：**
1. 二分找左边界
1. 二分找右边界
1. 返回[left, right]


## ⚠️ 易错点

- 找左边界时条件是 `nums[mid] >= target`（不是 `==`），找右边界时是 `nums[mid] <= target`（不是 `==`）。等号的方向决定了是"往左压"还是"往右压"。
- 最后必须验证 `first <= last`，否则当 `target` 不存在于数组中时，`first` 可能大于 `last`，返回的区间是无效的。
- 数组为空时直接返回 `[-1, -1]`，否则二分会越界。

- 找到target后不立即返回——继续搜索更靠左/右的位置

## 📊 复杂度分析

- 时间复杂度：`O(log n)`。跑了两次二分，每次 `O(log n)`。
- 空间复杂度：`O(1)`。只用了常数个变量。

## 🏢 实际业务应用

- 数据库的范围查询优化：B+ 树索引中查找某个值第一次和最后一次出现的位置，本质就是找左右边界，数据库用类似逻辑快速定位范围扫描的起止点。
- 日志系统中按时间范围查日志：找到某个时间戳对应的第一条和最后一条日志记录，需要对有序的时间戳数组做两次二分。
- 电商库存管理中查询某价格区间内的商品：在按价格排序的商品列表中，用左右边界二分快速定位区间起止位置。

- 数据库的范围查询优化：B+ 树索引中查找某个值第一次和最后一次出现的位置，本质就是找左右边界，数据库用类似逻辑快速定位范围扫描的起止点。
- 日志系统中按时间范围查日志：找到某个时间戳对应的第一条和最后一条日志记录，需要对有序的时间戳数组做两次二分。
- 电商库存管理中查询某价格区间内的商品：在按价格排序的商品列表中，用左右边界二分快速定位区间起止位置。

## 📖 形象类比

可以类比《水浒传》里宋江在聚义厅的名册中查找好汉的过程。

名册按好汉的绰号首字排序，同姓的好汉排在一起。宋江想找所有姓"李"的好汉在哪几页。他不会从头翻到尾，而是先从中间翻开：如果这一页是"李"，他继续往左翻，直到翻到第一个"李"之前的那一页，就找到了左边界。再从右边做同样的事，找到右边界。最后就能知道"李"姓好汉占了几页。

对应关系是：

- "名册按首字排序"对应排序数组
- "往左翻到第一个李之前"对应找左边界二分
- "往右翻到最后一个李之后"对应找右边界二分
- "占了几页"对应返回区间 `[first, last]`

可以类比《水浒传》里宋江在聚义厅的名册中查找好汉的过程。

名册按好汉的绰号首字排序，同姓的好汉排在一起。宋江想找所有姓"李"的好汉在哪几页。他不会从头翻到尾，而是先从中间翻开：如果这一页是"李"，他继续往左翻，直到翻到第一个"李"之前的那一页，就找到了左边界。再从右边做同样的事，找到右边界。最后就能知道"李"姓好汉占了几页。

对应关系是：

- "名册按首字排序"对应排序数组
- "往左翻到第一个李之前"对应找左边界二分
- "往右翻到最后一个李之后"对应找右边界二分
- "占了几页"对应返回区间 `[first, last]`

小鹿在小河边捡了一排编号石头，按编号排好，但有些编号重复了。老师问："编号 7 的石头从第几块到第几块？"小鹿不会一块块数，而是先从中间看：编号大于等于 7 就往左找，找到最左边的 7；再从中间看：编号小于等于 7 就往右找，找到最右边的 7。两次就搞定了。

小鹿在小河边捡了一排编号石头，按编号排好，但有些编号重复了。老师问："编号 7 的石头从第几块到第几块？"小鹿不会一块块数，而是先从中间看：编号大于等于 7 就往左找，找到最左边的 7；再从中间看：编号小于等于 7 就往右找，找到最右边的 7。两次就搞定了。

## 🎵 记忆口诀

等号往左压左界，往右压右界。

等号往左压左界，往右压右界。

## 🔗 延伸练习

- `35. 搜索插入位置`：只找左边界（第一个 `>= target` 的位置），不关心右边界，是本题的简化版。
- `704. 二分查找`：最基础的二分，没有重复元素，是本题的前置练习。

- `35. 搜索插入位置`：只找左边界（第一个 `>= target` 的位置），不关心右边界，是本题的简化版。
- `704. 二分查找`：最基础的二分，没有重复元素，是本题的前置练习。
