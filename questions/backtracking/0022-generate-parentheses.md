---
id: "0022"
slug: "generate-parentheses"
lcId: 22
title: "括号生成"
difficulty: "Medium"
category: "backtracking"
tags:
  - "字符串"
  - "动态规划"
  - "回溯"
url: "https://leetcode.cn/problems/generate-parentheses/"
planOrder: 59
hasViz: true
hasDiagram: false
feynman:
  essence: "给你 `n` 对括号，生成所有合法的括号组合。合法意味着每个左括号都有对应的右括号，且括号嵌套顺序正确。"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 22. 括号生成

> 难度：**Medium** | 分类：回溯 | 标签：字符串, 动态规划, 回溯

> 🔗 力扣链接：[https://leetcode.cn/problems/generate-parentheses/](https://leetcode.cn/problems/generate-parentheses/)

## 📝 题目描述

给你 `n` 对括号，生成所有合法的括号组合。合法意味着每个左括号都有对应的右括号，且括号嵌套顺序正确。

- 题号：22
- 题目名：括号生成
- 难度：中等
- 题型：回溯
- 为什么选这题：它是回溯法中"带约束的选择"的典型题，训练"合法状态剪枝"。

## 🧠 思考路径

回溯法的思路：在每一步决定放左括号还是右括号。但不是随便放——有两个约束：左括号数量不能超过 `n`，右括号数量不能超过左括号数量。

当前已用了 `left` 个左括号和 `right` 个右括号。如果 `left < n`，可以放左括号；如果 `right < left`，可以放右括号。当 `left == right == n` 时，得到一个合法组合。

## 💻 Java 题解

### 解法 1：回溯

open<n 时可以加左括号，close<open 时可以加右括号。open==close==n 时收集。

- ⏱ 时间复杂度：`O(4ⁿ/√n)`
- 💾 空间复杂度：`O(n)`

```java
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        backtrack(n, 0, 0, new StringBuilder(), result);
        return result;
    }
    private void backtrack(int n, int open, int close, StringBuilder sb, List<String> result) {
        if (sb.length() == 2 * n) { result.add(sb.toString()); return; }
        if (open < n) { sb.append('('); backtrack(n, open+1, close, sb, result); sb.deleteCharAt(sb.length()-1); }
        if (close < open) { sb.append(')'); backtrack(n, open, close+1, sb, result); sb.deleteCharAt(sb.length()-1); }
    }
}
```

**关键点：**
- open<n 才能加左括号
- close<open 才能加右括号
- sb.length()==2n 收集

**执行步骤：**
1. open<n→加左递归
1. close<open→加右递归
1. 回溯删除


## ⚠️ 易错点

- 右括号的条件是 `right < left`，不是 `right < n`。右括号不能比左括号多。
- Java 中 StringBuilder 要在递归返回后删掉最后一个字符（回溯）。
- `n = 0` 时返回空列表。

- close<open 不是 close<n——保证合法性

## 📊 复杂度分析

- 时间复杂度：`O(4^n / √n)`。第 n 个卡特兰数 `C_n ≈ 4^n / (n√n)`，每个组合构建需要 `O(n)`。
- 空间复杂度：`O(n)`。递归栈深度为 `2n`。

## 🏢 实际业务应用

- 合法嵌套结构生成：SQL 查询构建器中生成合法的嵌套条件表达式。
- 模板语法测试：自动生成各种嵌套结构的测试用例，验证解析器的正确性。
- 编程语言编译器：在语法分析阶段，合法括号序列的枚举用于测试语法的覆盖度。

- 合法嵌套结构生成：SQL 查询构建器中生成合法的嵌套条件表达式。
- 模板语法测试：自动生成各种嵌套结构的测试用例，验证解析器的正确性。
- 编程语言编译器：在语法分析阶段，合法括号序列的枚举用于测试语法的覆盖度。

## 📖 形象类比

可以类比《红楼梦》里开合礼制必须守规矩的场景。

贾府举办宴会，座位安排有严格的礼制规矩：每摆一列座位（左括号）就必须有对应的收尾席位（右括号），而且收尾不能早于开始。王熙凤负责安排，每次她可以选择"再开一列"或"收掉最近的一列"，但收掉时必须保证前面有未收的列。

对应关系是：

- "开一列座位"对应放左括号
- "收掉一列"对应放右括号
- "收掉时前面必须有未收的"对应 `right < left`
- "总共开 n 列"对应 `n` 对括号

记忆的关键是：左可以多，右不能超过左。

可以类比《红楼梦》里开合礼制必须守规矩的场景。

贾府举办宴会，座位安排有严格的礼制规矩：每摆一列座位（左括号）就必须有对应的收尾席位（右括号），而且收尾不能早于开始。王熙凤负责安排，每次她可以选择"再开一列"或"收掉最近的一列"，但收掉时必须保证前面有未收的列。

对应关系是：

- "开一列座位"对应放左括号
- "收掉一列"对应放右括号
- "收掉时前面必须有未收的"对应 `right < left`
- "总共开 n 列"对应 `n` 对括号

记忆的关键是：左可以多，右不能超过左。

小兔子在河边搭桥，每放一块红色桥板（左括号）就必须之后放一块蓝色桥板（右括号）来收尾。蓝色桥板只能搭在红色桥板之后。小兔子每一步可以选红色或蓝色，但蓝色不能比红色多。

小兔子在河边搭桥，每放一块红色桥板（左括号）就必须之后放一块蓝色桥板（右括号）来收尾。蓝色桥板只能搭在红色桥板之后。小兔子每一步可以选红色或蓝色，但蓝色不能比红色多。

## 🎵 记忆口诀

左不超n右不超左，两两相等就收走。

左不超n右不超左，两两相等就收走。

## 🔗 延伸练习

- `20. 有效的括号`：判断一个括号字符串是否合法。
- `32. 最长有效括号`：找最长的合法括号子串。

- `20. 有效的括号`：判断一个括号字符串是否合法。
- `32. 最长有效括号`：找最长的合法括号子串。
