---
id: "0208"
slug: "implement-trie-prefix-tree"
lcId: 208
title: "实现 Trie (前缀树)"
difficulty: "Medium"
category: "graph"
tags:
  - "设计"
  - "字典树"
  - "哈希表"
  - "字符串"
url: "https://leetcode.cn/problems/implement-trie-prefix-tree/"
planOrder: 54
hasViz: true
hasDiagram: false
feynman:
  essence: "实现一个 Trie（前缀树），支持三种操作：插入字符串 `insert`、搜索单词 `search`、判断前缀是否存在 `startsWith`。  重点不在\"会不会用现成的字典\"，而在\"怎么用一棵树"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 208. 实现 Trie (前缀树)

> 难度：**Medium** | 分类：图论 | 标签：设计, 字典树, 哈希表, 字符串

> 🔗 力扣链接：[https://leetcode.cn/problems/implement-trie-prefix-tree/](https://leetcode.cn/problems/implement-trie-prefix-tree/)

## 📝 题目描述

实现一个 Trie（前缀树），支持三种操作：插入字符串 `insert`、搜索单词 `search`、判断前缀是否存在 `startsWith`。

重点不在"会不会用现成的字典"，而在"怎么用一棵树把公共前缀压缩存储"。

- 题号：208
- 题目名：实现 Trie (前缀树)
- 难度：中等
- 题型：字典树
- 为什么选这题：它是字典树的标准实现题，掌握它就能理解搜索引擎、输入法联想背后的核心数据结构。

## 🧠 思考路径

如果用哈希表存所有单词，搜索单词是 `O(1)`，但判断前缀是否存在就很麻烦——你需要枚举所有可能的后续字符。而且空间浪费大，"abc"和"abd"的公共前缀"ab"存了两遍。

前缀树的思路是：把公共前缀合并到一条路径上。从根节点出发，每个节点有 26 个子节点槽位（对应 26 个字母）。插入一个单词时，沿着已有的路径走，走到没有对应字符的位置就创建新节点。在单词结束的节点上做一个标记，表示"到这里是一个完整的单词"。

搜索时沿着树走，如果走不通说明单词不存在；走通了但终点没有"完整单词"标记，说明这个序列只是某个更长单词的前缀。`startsWith` 只需要检查路径是否走得通，不要求终点有标记。

这题的关键词不是"存单词"，而是"用树共享公共前缀"。

## 💻 Java 题解

### 解法 1：标准Trie实现

每个节点维护children[26]和isEnd。insert逐字符创建节点，search和startsWith逐字符查找。

- ⏱ 时间复杂度：`O(m) per op`
- 💾 空间复杂度：`O(m×n)`

```java
class Trie {
    class Node { Node[] children = new Node[26]; boolean isEnd; }
    private Node root;
    public Trie() { root = new Node(); }
    public void insert(String word) {
        Node curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) curr.children[idx] = new Node();
            curr = curr.children[idx];
        }
        curr.isEnd = true;
    }
    public boolean search(String word) {
        Node node = find(word);
        return node != null && node.isEnd;
    }
    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }
    private Node find(String s) {
        Node curr = root;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) return null;
            curr = curr.children[idx];
        }
        return curr;
    }
}
```

**关键点：**
- children[26] 子节点数组
- isEnd 标记单词结束
- search vs startsWith 区别

**执行步骤：**
1. insert: 逐字符创建/遍历节点
1. search: 找到节点且isEnd=true
1. startsWith: 只需找到节点


## ⚠️ 易错点

- `search` 和 `startsWith` 的区别：前者要求路径走通 **且** 终点有标记；后者只要求路径走通。
- 插入时不要忘了在最后一个节点设 `is_end = True`，否则 `search` 永远返回 `False`。
- Java 用数组 `TrieNode[26]` 存子节点时，索引是 `c - 'a'`，注意输入只有小写字母。

- search 要检查 isEnd，startsWith 不需要

## 📊 复杂度分析

- 时间复杂度：`insert`、`search`、`startsWith` 均为 `O(L)`，`L` 为字符串长度。
- 空间复杂度：`O(N × L)`，`N` 为插入的单词数，`L` 为平均长度。公共前缀被共享，实际空间更优。

## 🏢 实际业务应用

- 搜索引擎的自动补全：用户每输入一个字符，就在 Trie 中走一步，实时返回以当前输入为前缀的所有建议词。
- 中文输入法的候选词联想：拼音序列映射到汉字，Trie 的路径匹配对应拼音输入，叶子节点对应候选词。
- 路由器的 IP 路由表查找：IP 前缀匹配和最长前缀匹配，本质上就是 Trie 的路径搜索。

- 搜索引擎的自动补全：用户每输入一个字符，就在 Trie 中走一步，实时返回以当前输入为前缀的所有建议词。
- 中文输入法的候选词联想：拼音序列映射到汉字，Trie 的路径匹配对应拼音输入，叶子节点对应候选词。
- 路由器的 IP 路由表查找：IP 前缀匹配和最长前缀匹配，本质上就是 Trie 的路径搜索。

## 📖 形象类比

可以把它类比成《三国演义》里曹操的"地名索引"系统。

曹操每攻下一座城，就让书记官在一张大地图上标出路线：从许都出发，经过哪些关口到达这座城。如果两座城前半段路相同（公共前缀），就共用同一条路线标记，只在分叉处标出不同方向。查某条路是否存在，就像 `startsWith`；查这条路终点是不是一座具体的城（而不是只到某个关口），就像 `search`。

对应关系是：

- "Trie 的根节点"对应许都（出发点）
- "每条路径"对应从许都出发的行军路线
- "公共前缀"对应多支军队共享的同一段路
- "is_end 标记"对应路线终点是一座城（而非中途关口）
- "search"对应查某条路是否通到具体城池
- "startsWith"对应查某条路至少通到某个关口

这段记忆的关键是：相同的路只走一遍，在分叉处才分开。

可以把它类比成《三国演义》里曹操的"地名索引"系统。

曹操每攻下一座城，就让书记官在一张大地图上标出路线：从许都出发，经过哪些关口到达这座城。如果两座城前半段路相同（公共前缀），就共用同一条路线标记，只在分叉处标出不同方向。查某条路是否存在，就像 `startsWith`；查这条路终点是不是一座具体的城（而不是只到某个关口），就像 `search`。

对应关系是：

- "Trie 的根节点"对应许都（出发点）
- "每条路径"对应从许都出发的行军路线
- "公共前缀"对应多支军队共享的同一段路
- "is_end 标记"对应路线终点是一座城（而非中途关口）
- "search"对应查某条路是否通到具体城池
- "startsWith"对应查某条路至少通到某个关口

这段记忆的关键是：相同的路只走一遍，在分叉处才分开。

小蚂蚁在泥土里挖了一套地下通道，每条通道用字母标记。当多只蚂蚁都要去类似的目的地（比如 "apple" 和 "app"），它们共享前半段通道 "a-p-p"，在最后才各挖各的。每到一个终点，蚂蚁就放一颗小石子做标记（is_end），这样后来者一看就知道："这条路走得通，而且这里是个完整的目的地，不只是个中转站。"

小蚂蚁在泥土里挖了一套地下通道，每条通道用字母标记。当多只蚂蚁都要去类似的目的地（比如 "apple" 和 "app"），它们共享前半段通道 "a-p-p"，在最后才各挖各的。每到一个终点，蚂蚁就放一颗小石子做标记（is_end），这样后来者一看就知道："这条路走得通，而且这里是个完整的目的地，不只是个中转站。"

## 🎵 记忆口诀

沿路走，不通就建；终点加标记，搜索看标记。

沿路走，不通就建；终点加标记，搜索看标记。

## 🔗 延伸练习

- `211. 添加与搜索单词`：本题的进阶版，搜索时支持通配符 `.`,需要回溯搜索所有子节点。
- `212. 单词搜索 II`：Trie + DFS 回溯的组合，在二维网格中批量查找单词。

- `211. 添加与搜索单词`：本题的进阶版，搜索时支持通配符 `.`,需要回溯搜索所有子节点。
- `212. 单词搜索 II`：Trie + DFS 回溯的组合，在二维网格中批量查找单词。
