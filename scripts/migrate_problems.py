#!/usr/bin/env python3
"""迁移 100 题：legacy/js/problems-data.js + sol-v2-*.js → questions/<cat>/00XX-slug.md

输出 markdown 带 frontmatter（id/slug/lcId/title/difficulty/category/tags/url/
planOrder/hasViz/hasDiagram/feynman/first_principle），正文含题目标题、
力扣链接、题解 thinking。
"""
import re
import os
import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LEGACY = os.path.join(ROOT, 'legacy', 'js')
OUT = os.path.join(ROOT, 'questions')

CAT_MAP = {
    '哈希': 'hash', '双指针': 'two-pointers', '滑动窗口': 'sliding-window',
    '子串': 'substring', '普通数组': 'array', '矩阵': 'matrix',
    '链表': 'linked-list', '二叉树': 'binary-tree', '图论': 'graph',
    '回溯': 'backtracking', '二分查找': 'binary-search', '栈': 'stack',
    '堆': 'heap', '贪心算法': 'greedy', '动态规划': 'dynamic-programming',
    '多维动态规划': 'multi-dp', '技巧': 'techniques',
}

# 13 题有 SVG 图解（见 legacy README）
DIAGRAM_IDS = {'1', '3', '15', '42', '53', '141', '206', '94', '102', '20', '200', '215', '70'}


def _parse_quoted_string(raw, start):
    """从 raw[start]（应为引号）开始解析 JS 字符串字面量，返回 (value, end_index)。
    支持 "..." 和 '...'，处理反斜杠转义。"""
    quote = raw[start]
    assert quote in ('"', "'"), f"expected quote at {start}, got {quote!r}"
    i = start + 1
    out = []
    while i < len(raw):
        ch = raw[i]
        if ch == '\\' and i + 1 < len(raw):
            nxt = raw[i + 1]
            mapping = {'n': '\n', 't': '\t', 'r': '\r', '"': '"', "'": "'", '\\': '\\', '/': '/', '`': '`'}
            out.append(mapping.get(nxt, nxt))
            i += 2
            continue
        if ch == quote:
            return ''.join(out), i + 1
        out.append(ch)
        i += 1
    raise ValueError("unterminated string literal")


def parse_problems():
    """解析 problems-data.js 中的 {id:"1",slug:"...",...} 条目。"""
    raw = open(os.path.join(LEGACY, 'problems-data.js'), encoding='utf-8').read()
    problems = []
    for m in re.finditer(r'\{id:', raw):
        # 找到匹配的右大括号
        start = m.start()
        depth = 0
        i = start
        while i < len(raw):
            if raw[i] == '{':
                depth += 1
            elif raw[i] == '}':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        block = raw[start:i + 1]

        def field(name, pat):
            mm = re.search(pat, block)
            return mm.group(1) if mm else ''

        # id
        pid = field('id', r'id:\s*"([^"]+)"')
        slug = field('slug', r'slug:\s*"([^"]+)"')
        title = field('title', r'title:\s*"([^"]+)"')
        diff = field('diff', r'diff:\s*"([^"]+)"')
        cat = field('cat', r'cat:\s*"([^"]+)"')
        url = field('url', r'url:\s*"([^"]+)"')
        # tags：提取方括号内所有引号字符串
        tags_m = re.search(r'tags:\s*\[(.*?)\]', block, re.S)
        tags = re.findall(r'"([^"]+)"', tags_m.group(1)) if tags_m else []
        problems.append({
            'id': pid, 'slug': slug, 'title': title, 'diff': diff,
            'cat': cat, 'url': url, 'tags': tags,
        })
    return problems


def parse_solutions():
    """读所有 sol-v2-*.js，提取每个 SOLUTIONS["id"] 块的 thinking 字段。"""
    sols = {}
    for f in sorted(glob.glob(os.path.join(LEGACY, 'sol-v2-*.js'))):
        raw = open(f, encoding='utf-8').read()
        for m in re.finditer(r'SOLUTIONS\["(\d+)"\]\s*=\s*\{', raw):
            pid = m.group(1)
            brace_start = m.end() - 1  # 指向 '{'
            depth = 0
            i = brace_start
            while i < len(raw):
                if raw[i] == '{':
                    depth += 1
                elif raw[i] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            block = raw[brace_start:i + 1]
            # 找 thinking: "..." 或 thinking: `...`
            tm = re.search(r'thinking:\s*(["\'`])', block)
            thinking = ''
            if tm:
                val, _ = _parse_quoted_string(block, tm.start(1))
                thinking = val.strip()
            sols[pid] = {'thinking': thinking}
    return sols


def yaml_escape(s):
    """YAML 双引号字符串转义。"""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')


def main():
    problems = parse_problems()
    sols = parse_solutions()
    print(f"parsed {len(problems)} problems, {len(sols)} solutions")

    total = 0
    for order, p in enumerate(problems, 1):
        cat_dir = CAT_MAP.get(p['cat'], 'other')
        os.makedirs(os.path.join(OUT, cat_dir), exist_ok=True)
        try:
            fname = f"{int(p['id']):04d}-{p['slug']}.md"
        except ValueError:
            fname = f"{order:04d}-{p['slug']}.md"
        path = os.path.join(OUT, cat_dir, fname)

        sol = sols.get(p['id'], {})
        thinking = sol.get('thinking', '')
        has_diag = p['id'] in DIAGRAM_IDS

        tags_lines = '\n'.join(f'  - "{yaml_escape(t)}"' for t in p['tags']) if p['tags'] else '  []'
        feynman_essence = yaml_escape(thinking[:80]) if thinking else ''

        fm = []
        fm.append('---')
        fm.append(f'id: "{int(p["id"]):04d}"')
        fm.append(f'slug: "{p["slug"]}"')
        fm.append(f'lcId: {p["id"]}')
        fm.append(f'title: "{yaml_escape(p["title"])}"')
        fm.append(f'difficulty: "{p["diff"]}"')
        fm.append(f'category: "{cat_dir}"')
        fm.append('tags:')
        fm.append(tags_lines)
        fm.append(f'url: "{p["url"]}"')
        fm.append(f'planOrder: {order}')
        fm.append(f'hasViz: true')
        fm.append(f'hasDiagram: {"true" if has_diag else "false"}')
        fm.append('feynman:')
        fm.append(f'  essence: "{feynman_essence}"')
        fm.append('  analogy: ""')
        fm.append('  key_points: []')
        fm.append('first_principle:')
        fm.append('  problem: ""')
        fm.append('  axioms: []')
        fm.append('  rebuild: ""')
        fm.append('---')
        fm.append('')
        fm.append(f'# {p["id"]}. {p["title"]}')
        fm.append('')
        fm.append(f'> 难度：{p["diff"]} | 分类：{p["cat"]} | 标签：{", ".join(p["tags"])}')
        fm.append(f'> 力扣链接：[{p["url"]}]({p["url"]})')
        fm.append('')
        fm.append('## 题目描述')
        fm.append('')
        fm.append('（待从力扣补充题目描述与示例）')
        fm.append('')
        fm.append('## 题解')
        fm.append('')
        if thinking:
            fm.append(thinking)
            fm.append('')
            fm.append('> 多解法、复杂度分析、关键点与陷阱详见弹窗内的解法面板（由 legacy sol-v2 数据驱动）。')
        else:
            fm.append('（题解详见弹窗内的解法面板，由 legacy sol-v2 数据驱动）')
        fm.append('')

        open(path, 'w', encoding='utf-8').write('\n'.join(fm))
        total += 1

    print(f"migrated {total} problems to {OUT}")

    # 统计
    cats = set()
    for p in problems:
        cats.add(CAT_MAP.get(p['cat'], 'other'))
    print(f"categories: {len(cats)}")


if __name__ == '__main__':
    main()
