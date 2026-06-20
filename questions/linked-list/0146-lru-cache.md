---
id: "0146"
slug: "lru-cache"
lcId: 146
title: "LRU 缓存"
difficulty: "Medium"
category: "linked-list"
tags:
  - "设计"
  - "哈希表"
  - "链表"
  - "双向链表"
url: "https://leetcode.cn/problems/lru-cache/"
planOrder: 35
hasViz: true
hasDiagram: false
feynman:
  essence: "请你设计并实现一个 LRU（最近最少使用）缓存机制。它应该支持以下操作： - `get(key)`：如果 `key` 存在缓存中，返回其值，并将其移到\"最近使用\"的位置；否则返回 -1。 - `put"
  analogy: ""
  key_points: []
first_principle:
  problem: ""
  axioms: []
  rebuild: ""
---

# 146. LRU 缓存

> 难度：**Medium** | 分类：链表 | 标签：设计, 哈希表, 链表, 双向链表

> 🔗 力扣链接：[https://leetcode.cn/problems/lru-cache/](https://leetcode.cn/problems/lru-cache/)

## 📝 题目描述

请你设计并实现一个 LRU（最近最少使用）缓存机制。它应该支持以下操作：
- `get(key)`：如果 `key` 存在缓存中，返回其值，并将其移到"最近使用"的位置；否则返回 -1。
- `put(key, value)`：如果 `key` 存在，更新其值并移到"最近使用"；如果不存在，插入新的键值对。如果插入后超出容量，淘汰"最久未使用"的那个。

要求 `get` 和 `put` 都是 `O(1)` 时间复杂度。重点不在"缓存是什么"，而在"怎么在 `O(1)` 内同时做到查找、插入和按使用顺序排列"。

- 题号：146
- 题目名：LRU 缓存
- 难度：中等
- 题型：设计
- 为什么选这题：它是数据结构设计的标杆题，哈希表 + 双向链表的组合是工业级缓存的基础实现。

## 🧠 思考路径

要实现 `O(1)` 的查找，哈希表是第一选择。但哈希表本身没有"顺序"的概念——怎么知道哪个键最久没用？

我们需要一个有序的数据结构，能快速把一个元素移到"最近使用"的位置（头部），以及快速淘汰"最久未使用"的元素（尾部）。双向链表可以做到：移到头部只需要断开节点再插入头部，都是 `O(1)`。

但链表查找是 `O(n)`，所以我们用哈希表来存 `key → 链表节点` 的映射。这样：
- 查找：哈希表 `O(1)` 找到节点，然后把节点移到链表头部。
- 插入：新节点加到链表头部，存入哈希表；超容量时删除链表尾部，同时从哈希表中移除。

所以这题的关键词不是"缓存"，而是"哈希表管查找，双向链表管顺序，两者配合实现 O(1)"。

## 💻 Java 题解

### 解法 1：HashMap + 双向链表

HashMap 提供 O(1) 查找，双向链表维护 LRU 顺序。最近访问的放头部，尾部是最久未使用的。

- ⏱ 时间复杂度：`O(1) get/put`
- 💾 空间复杂度：`O(capacity)`

```java
class LRUCache {
    class DNode {
        int key, val; DNode prev, next;
        DNode(int k, int v) { key = k; val = v; }
    }
    private int capacity;
    private Map<Integer, DNode> map = new HashMap<>();
    private DNode head, tail; // dummy

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head = new DNode(0, 0);
        tail = new DNode(0, 0);
        head.next = tail; tail.prev = head;
    }
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        DNode node = map.get(key);
        moveToHead(node);
        return node.val;
    }
    public void put(int key, int value) {
        if (map.containsKey(key)) {
            DNode node = map.get(key);
            node.val = value;
            moveToHead(node);
        } else {
            DNode node = new DNode(key, value);
            map.put(key, node);
            addToHead(node);
            if (map.size() > capacity) {
                DNode lru = tail.prev;
                removeNode(lru);
                map.remove(lru.key);
            }
        }
    }
    private void addToHead(DNode node) {
        node.next = head.next; node.prev = head;
        head.next.prev = node; head.next = node;
    }
    private void removeNode(DNode node) {
        node.prev.next = node.next; node.next.prev = node.prev;
    }
    private void moveToHead(DNode node) {
        removeNode(node); addToHead(node);
    }
}
```

**关键点：**
- HashMap + 双向链表
- dummy head 和 tail 简化边界
- get/put 都是 O(1)

**执行步骤：**
1. get: HashMap 查找 → moveToHead
1. put: 新建→addToHead→超容量删 tail.prev
1. head 端是最近访问，tail 端是最久未用


## ⚠️ 易错点

- 必须用双向链表，单向链表无法 `O(1)` 删除节点（因为需要知道前驱）。
- 哨兵节点可以避免大量 `null` 判断，是工业级写法的标配。
- 淘汰尾部时，除了从链表删除，还必须从哈希表中 `del/delete` 对应的 key。
- 节点里要存 `key`，否则淘汰时不知道该从哈希表里删除哪个 key。

- 双向链表需要 dummy head/tail 避免 null 判断

- 删除时要从 map 中也删除

## 📊 复杂度分析

- 时间复杂度：`get` 和 `put` 都是 `O(1)`。哈希表查找 `O(1)`，链表操作 `O(1)`。
- 空间复杂度：`O(capacity)`。哈希表和链表最多存 capacity 个节点。

## 🏢 实际业务应用

- Redis 的内存淘汰策略之一就是 LRU，当内存不够时优先淘汰最久没访问的 key。
- 操作系统的页面置换：物理内存不够时，把最久没使用的页面换出到磁盘。
- 浏览器的缓存策略：缓存的图片、CSS 等资源按 LRU 淘汰，保证最近使用的资源快速加载。
- 数据库的缓冲池（Buffer Pool）：MySQL 的 InnoDB 用 LRU 变体管理数据页的缓存。

- Redis 的内存淘汰策略之一就是 LRU，当内存不够时优先淘汰最久没访问的 key。
- 操作系统的页面置换：物理内存不够时，把最久没使用的页面换出到磁盘。
- 浏览器的缓存策略：缓存的图片、CSS 等资源按 LRU 淘汰，保证最近使用的资源快速加载。
- 数据库的缓冲池（Buffer Pool）：MySQL 的 InnoDB 用 LRU 变体管理数据页的缓存。

## 📖 形象类比

可以把它类比成《红楼梦》里贾母的书房。

书房只能放固定数量的字画（容量）。每幅字画上贴了标签（key）。贾母每次看一幅（get），就把它挪到最前面；新买的字画（put）也放最前面。书房满了的时候，最久没被翻看的那幅（链表尾部）就被收进库房。管家手里有一本名册（哈希表），翻名册就能立刻找到对应字画的位置。

对应关系是：

- "书房"对应缓存，容量有限
- "字画"对应缓存中的键值对
- "挪到最前面"对应 `moveToHead`
- "最久没被翻看就收走"对应 `removeTail`
- "名册"对应哈希表，O(1) 查找
- "字画挂绳前后相连"对应双向链表

这段记忆的关键是：哈希表管"能不能找到"，链表管"谁最近用过"。

可以把它类比成《红楼梦》里贾母的书房。

书房只能放固定数量的字画（容量）。每幅字画上贴了标签（key）。贾母每次看一幅（get），就把它挪到最前面；新买的字画（put）也放最前面。书房满了的时候，最久没被翻看的那幅（链表尾部）就被收进库房。管家手里有一本名册（哈希表），翻名册就能立刻找到对应字画的位置。

对应关系是：

- "书房"对应缓存，容量有限
- "字画"对应缓存中的键值对
- "挪到最前面"对应 `moveToHead`
- "最久没被翻看就收走"对应 `removeTail`
- "名册"对应哈希表，O(1) 查找
- "字画挂绳前后相连"对应双向链表

这段记忆的关键是：哈希表管"能不能找到"，链表管"谁最近用过"。

小松鼠有一个小树洞当粮仓，只能放 10 颗松果。每拿一颗松果出来吃，它就把这颗放到洞口最近的位置。新采的松果也放洞口。如果洞满了，最里面那颗最久没碰过的松果就被搬出来放到外面。小松鼠还有一本小册子，上面记着每种松果放在第几个格子里——一翻册子就知道在哪，不用一个格子一个格子找。

小松鼠有一个小树洞当粮仓，只能放 10 颗松果。每拿一颗松果出来吃，它就把这颗放到洞口最近的位置。新采的松果也放洞口。如果洞满了，最里面那颗最久没碰过的松果就被搬出来放到外面。小松鼠还有一本小册子，上面记着每种松果放在第几个格子里——一翻册子就知道在哪，不用一个格子一个格子找。

## 🎵 记忆口诀

哈希管查找，链表管顺序；最近用放头，最久没用删尾。

哈希管查找，链表管顺序；最近用放头，最久没用删尾。

## 🔗 延伸练习

- `460. LFU 缓存`：从"最久没用"变成"最少使用"，难度更高，需要两层频率管理。
- `138. 随机链表的复制`：同样是哈希表 + 链表的组合，但侧重复制而非设计。

- `460. LFU 缓存`：从"最久没用"变成"最少使用"，难度更高，需要两层频率管理。
- `138. 随机链表的复制`：同样是哈希表 + 链表的组合，但侧重复制而非设计。
