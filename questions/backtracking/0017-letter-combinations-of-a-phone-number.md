---
id: "0017"
slug: "letter-combinations-of-a-phone-number"
lcId: 17
title: "电话号码的字母组合"
difficulty: "Medium"
category: "backtracking"
tags:
  - "哈希表"
  - "字符串"
  - "回溯"
url: "https://leetcode.cn/problems/letter-combinations-of-a-phone-number/"
planOrder: 57
hasViz: true
hasDiagram: false
feynman:
  essence: "给你一个数字字符串（如 `\"23\"`），每个数字对应手机键盘上的几个字母（2→abc, 3→def...）。返回所有可能的字母组合。  比如 `\"23\"` 对应 `[\"ad\",\"ae\",\"af\",\"b"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 17. 电话号码的字母组合

> 难度：**Medium** | 分类：回溯 | 标签：哈希表, 字符串, 回溯

> 🔗 力扣链接：[https://leetcode.cn/problems/letter-combinations-of-a-phone-number/](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)

## 📝 题目描述

给你一个数字字符串（如 `"23"`），每个数字对应手机键盘上的几个字母（2→abc, 3→def...）。返回所有可能的字母组合。

比如 `"23"` 对应 `["ad","ae","af","bd","be","bf","cd","ce","cf"]`。

- 题号：17
- 题目名：电话号码的字母组合
- 难度：中等
- 题型：回溯
- 为什么选这题：它是回溯法最直观的入门题，"在每一步做选择"的框架非常清晰。

## 🧠 思考路径

每一位数字有 3-4 个字母可选，所有组合就是每个位置的选择做笛卡尔积。最自然的做法是递归/回溯：处理第 `i` 位数字时，枚举它对应的所有字母，分别拼上去，然后递归处理下一位。

当处理完所有数字位时，当前拼接的字符串就是一个合法组合。

## 💻 Java 题解

### 解法 1：回溯

用数组存数字到字母的映射，回溯枚举每个数字对应的字母。

- ⏱ 时间复杂度：`O(3ⁿ×4ᵐ)`
- 💾 空间复杂度：`O(n)`

```java
class Solution {
    private String[] mapping = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    public List<String> letterCombinations(String digits) {
        List<String> result = new ArrayList<>();
        if (digits.isEmpty()) return result;
        backtrack(digits, 0, new StringBuilder(), result);
        return result;
    }
    private void backtrack(String digits, int idx, StringBuilder sb, List<String> result) {
        if (idx == digits.length()) { result.add(sb.toString()); return; }
        String letters = mapping[digits.charAt(idx) - '0'];
        for (char c : letters.toCharArray()) {
            sb.append(c);
            backtrack(digits, idx + 1, sb, result);
            sb.deleteCharAt(sb.length() - 1);
        }
    }
}
```

**关键点：**
- 数字到字母映射
- idx==digits.length() 收集结果
- StringBuilder append/delete 回溯

**执行步骤：**
1. 取当前数字对应的字母
1. 遍历每个字母
1. 递归+回溯


## ⚠️ 易错点

- 空字符串要返回空列表，不是包含空字符串的列表。
- 数字 `1` 和 `0` 没有对应字母，题目保证输入只含 `2-9`。
- Java 中 StringBuilder 要在递归返回后 `deleteCharAt`（回溯），Python 中 `path + ch` 自动创建新字符串，不需要手动回退。

- 空字符串返回空列表不是返回['']

- StringBuilder 要回溯删除

## 📊 复杂度分析

- 时间复杂度：`O(4^n × n)`。`n` 是数字位数，每位最多 4 个字母，总共 `4^n` 种组合，每种组合构建需要 `O(n)`。
- 空间复杂度：`O(n)`。递归栈深度为 `n`。

## 🏢 实际业务应用

- 输入法候选生成：手机九宫格输入法中，用户按数字键后生成所有可能的拼音组合。
- 编码映射：在某些编码系统中，数字编码对应多义字符，需要枚举所有可能的解码结果。
- 密码组合枚举：安全测试中，根据已知的数字密码模式生成所有可能的字母组合。

- 输入法候选生成：手机九宫格输入法中，用户按数字键后生成所有可能的拼音组合。
- 编码映射：在某些编码系统中，数字编码对应多义字符，需要枚举所有可能的解码结果。
- 密码组合枚举：安全测试中，根据已知的数字密码模式生成所有可能的字母组合。

## 📖 形象类比

可以类比《西游记》里唐僧念咒语解锁法术的场景。

唐僧手里有一串数字牌，每块牌上写着 2-9 的数字，每个数字对应几个梵文字符。他需要把每块牌上的字符挑一个拼在一起，形成一句完整的咒语。他从第一块牌开始，依次试每个字符，每选一个就往下一个牌看。所有牌都选完了，一句咒语就成型了。

对应关系是：

- "数字牌序列"对应 `digits`
- "每块牌上的可选字符"对应 `mapping`
- "每块牌挑一个"对应回溯的枚举
- "完整的咒语"对应一个字母组合

记忆的关键是：逐位枚举，每选一个往下递归，到底就记录。

可以类比《西游记》里唐僧念咒语解锁法术的场景。

唐僧手里有一串数字牌，每块牌上写着 2-9 的数字，每个数字对应几个梵文字符。他需要把每块牌上的字符挑一个拼在一起，形成一句完整的咒语。他从第一块牌开始，依次试每个字符，每选一个就往下一个牌看。所有牌都选完了，一句咒语就成型了。

对应关系是：

- "数字牌序列"对应 `digits`
- "每块牌上的可选字符"对应 `mapping`
- "每块牌挑一个"对应回溯的枚举
- "完整的咒语"对应一个字母组合

记忆的关键是：逐位枚举，每选一个往下递归，到底就记录。

小兔子拿到一串铃铛，每个铃铛上刻着数字。每个数字对应几片不同颜色的花瓣。小兔子从第一个铃铛开始，挑一片花瓣别在绳子上，再看下一个铃铛。所有铃铛都挑完了，就编好一条花链。

小兔子拿到一串铃铛，每个铃铛上刻着数字。每个数字对应几片不同颜色的花瓣。小兔子从第一个铃铛开始，挑一片花瓣别在绳子上，再看下一个铃铛。所有铃铛都挑完了，就编好一条花链。

## 🎵 记忆口诀

逐位选字母，到底就收走。

逐位选字母，到底就收走。

## 🔗 延伸练习

- `39. 组合总和`：从"固定位置选一个"变成"选一个数然后递归找和等于目标"。
- `78. 子集`：从"每个位置必须选"变成"每个元素选或不选"。

- `39. 组合总和`：从"固定位置选一个"变成"选一个数然后递归找和等于目标"。
- `78. 子集`：从"每个位置必须选"变成"每个元素选或不选"。
