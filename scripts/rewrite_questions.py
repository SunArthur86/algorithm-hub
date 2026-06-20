#!/usr/bin/env python3
"""重写 100 题 markdown：合并 参考目录 + legacy Java 题解。

数据来源：
  1. legacy/js/problems-data.js  — 元数据（id/slug/title/diff/cat/tags/url）
  2. legacy/js/sol-v2-*.js       — Java 题解（thinking + approaches[name/desc/complexity/code/keyPoints/steps] + pitfalls）
  3. ~/work/ai/vibe-algrithm-all/<id>-<slug>.md — 参考内容（题意翻译/思考路径/易错点/复杂度/业务应用/名著类比/森林故事/记忆口诀/延伸练习）

输出 questions/<cat>/00XX-slug.md，正文为富 markdown：
  题目描述（参考题意翻译）+ 思考路径 + Java 题解（多解法）+ 易错点
  + 复杂度 + 业务应用 + 名著类比 + 记忆口诀 + 延伸练习
frontmatter 保留 feynman/first_principle（从 thinking/参考推导）。
"""
import os
import re
import glob
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LEGACY = os.path.join(ROOT, 'legacy', 'js')
REF_DIR = os.path.expanduser('~/work/ai/vibe-algrithm-all')
OUT = os.path.join(ROOT, 'questions')

CAT_MAP = {
    '哈希': 'hash', '双指针': 'two-pointers', '滑动窗口': 'sliding-window',
    '子串': 'substring', '普通数组': 'array', '矩阵': 'matrix',
    '链表': 'linked-list', '二叉树': 'binary-tree', '图论': 'graph',
    '回溯': 'backtracking', '二分查找': 'binary-search', '栈': 'stack',
    '堆': 'heap', '贪心算法': 'greedy', '动态规划': 'dynamic-programming',
    '多维动态规划': 'multi-dp', '技巧': 'techniques',
}
DIAGRAM_IDS = {'1', '3', '15', '42', '53', '141', '206', '94', '102', '20', '200', '215', '70'}


# ---------- legacy 解析 ----------

def parse_problems():
    raw = open(os.path.join(LEGACY, 'problems-data.js'), encoding='utf-8').read()
    out = []
    for m in re.finditer(r'\{id:', raw):
        start = m.start()
        depth = 0
        i = start
        while i < len(raw):
            if raw[i] == '{': depth += 1
            elif raw[i] == '}':
                depth -= 1
                if depth == 0: break
            i += 1
        block = raw[start:i + 1]

        def field(name, pat):
            mm = re.search(pat, block)
            return mm.group(1) if mm else ''
        pid = field('id', r'id:\s*"([^"]+)"')
        slug = field('slug', r'slug:\s*"([^"]+)"')
        title = field('title', r'title:\s*"([^"]+)"')
        diff = field('diff', r'diff:\s*"([^"]+)"')
        cat = field('cat', r'cat:\s*"([^"]+)"')
        url = field('url', r'url:\s*"([^"]+)"')
        tags_m = re.search(r'tags:\s*\[(.*?)\]', block, re.S)
        tags = re.findall(r'"([^"]+)"', tags_m.group(1)) if tags_m else []
        out.append({'id': pid, 'slug': slug, 'title': title, 'diff': diff,
                    'cat': cat, 'url': url, 'tags': tags})
    return out


def _parse_js_value(raw, start):
    """从 raw[start] 开始解析 JS 值（字符串/数组/对象/模板字面量），返回 (python_value, end)。"""
    i = start
    while i < len(raw) and raw[i] in ' \t\n\r': i += 1
    ch = raw[i]
    if ch == '`':
        # 模板字面量
        j = i + 1
        buf = []
        while j < len(raw):
            if raw[j] == '\\' and j + 1 < len(raw):
                buf.append(raw[j + 1]); j += 2; continue
            if raw[j] == '`': return ''.join(buf), j + 1
            buf.append(raw[j]); j += 1
        return ''.join(buf), j
    if ch in ('"', "'"):
        j = i + 1
        buf = []
        while j < len(raw):
            if raw[j] == '\\' and j + 1 < len(raw):
                nxt = raw[j + 1]
                buf.append({'n': '\n', 't': '\t', 'r': '\r'}.get(nxt, nxt))
                j += 2; continue
            if raw[j] == ch: return ''.join(buf), j + 1
            buf.append(raw[j]); j += 1
        return ''.join(buf), j
    if ch == '[':
        arr = []; j = i + 1
        while j < len(raw):
            while j < len(raw) and raw[j] in ' \t\n\r,': j += 1
            if j >= len(raw) or raw[j] == ']': return arr, j + 1
            val, j = _parse_js_value(raw, j)
            arr.append(val)
        return arr, j
    if ch == '{':
        obj = {}; j = i + 1
        while j < len(raw):
            while j < len(raw) and raw[j] in ' \t\n\r,': j += 1
            if j >= len(raw) or raw[j] == '}': return obj, j + 1
            # key:
            km = re.match(r'(\w+)\s*:\s*', raw[j:])
            if not km: j += 1; continue
            key = km.group(1)
            j += km.end()
            val, j = _parse_js_value(raw, j)
            obj[key] = val
        return obj, j
    # 裸值（数字/标识符）
    jm = re.match(r'[^\s,}\]]+', raw[i:])
    return (jm.group(0) if jm else ''), i + (jm.end() if jm else 0)


def parse_solutions():
    sols = {}
    for f in sorted(glob.glob(os.path.join(LEGACY, 'sol-v2-*.js'))):
        raw = open(f, encoding='utf-8').read()
        for m in re.finditer(r'SOLUTIONS\["(\d+)"\]\s*=\s*', raw):
            pid = m.group(1)
            brace = raw.find('{', m.end())
            obj, _ = _parse_js_value(raw, brace)
            sols[pid] = obj
    return sols


# ---------- 参考目录解析 ----------

def parse_reference(lc_id):
    """读 ~/work/ai/vibe-algrithm-all/<id>-*.md，按 ## 分节返回 dict。"""
    matches = glob.glob(os.path.join(REF_DIR, f'{lc_id}-*.md'))
    if not matches:
        # 部分文件可能 0 开头
        matches = glob.glob(os.path.join(REF_DIR, f'{int(lc_id)}-*.md'))
    if not matches:
        return None
    raw = open(matches[0], encoding='utf-8').read()
    sections = {}
    # 按 ## 标题分块
    parts = re.split(r'\n(##\s+[^\n]+)\n', raw)
    # parts[0] 是第一个 ## 之前的内容（含 # 主标题）
    sections['_intro'] = parts[0].strip()
    for k in range(1, len(parts) - 1, 2):
        heading = parts[k].strip()
        body = parts[k + 1].strip()
        # 提取标题里的数字/名字（如 "## 2. 题意翻译" -> "题意翻译"）
        label = re.sub(r'^##\s+\d+\.\s*', '', heading)
        sections[label] = body
    return sections


def extract_sections(ref, *names):
    """从参考 dict 取多个节，拼接（跳过缺失）。"""
    out = []
    for n in names:
        for key, body in (ref or {}).items():
            if n in key:
                out.append(body)
                break
    return '\n\n'.join(out)


# ---------- 输出 ----------

def yaml_esc(s):
    if not s: return ''
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').strip()


def build_body(p, sol, ref):
    """组装正文 markdown。"""
    parts = []

    # 题目描述：优先用参考的"题意翻译"
    desc = extract_sections(ref, '题意翻译', '题目卡片')
    if desc:
        parts.append('## 📝 题目描述\n\n' + desc)
    else:
        parts.append('## 📝 题目描述\n\n请参考[力扣原题](' + p['url'] + ')。')

    # 思考路径
    thinking_ref = extract_sections(ref, '思考路径')
    legacy_thinking = sol.get('thinking', '') if sol else ''
    if thinking_ref:
        parts.append('## 🧠 思考路径\n\n' + thinking_ref)
    elif legacy_thinking:
        parts.append('## 🧠 思考路径\n\n' + legacy_thinking)

    # Java 题解（来自 legacy approaches）
    approaches = sol.get('approaches', []) if sol else []
    if approaches:
        sol_parts = ['## 💻 Java 题解']
        for idx, ap in enumerate(approaches, 1):
            name = ap.get('name', f'解法 {idx}')
            sol_parts.append(f'\n### 解法 {idx}：{name}\n')
            desc_ap = ap.get('desc', '')
            if desc_ap:
                sol_parts.append(desc_ap + '\n')
            cx = ap.get('complexity', {})
            if isinstance(cx, dict) and (cx.get('time') or cx.get('space')):
                sol_parts.append(f"- ⏱ 时间复杂度：`{cx.get('time', '?')}`")
                sol_parts.append(f"- 💾 空间复杂度：`{cx.get('space', '?')}`\n")
            code = ap.get('code', '')
            lang = ap.get('lang', 'java')
            if code:
                sol_parts.append(f'```{lang}\n{code}\n```\n')
            kp = ap.get('keyPoints', [])
            if kp:
                sol_parts.append('**关键点：**')
                for k in kp:
                    sol_parts.append(f'- {k}')
                sol_parts.append('')
            steps = ap.get('steps', [])
            if steps:
                sol_parts.append('**执行步骤：**')
                for s in steps:
                    sol_parts.append(f'1. {s}')
                sol_parts.append('')
        parts.append('\n'.join(sol_parts))

    # 易错点（legacy pitfalls + 参考）
    pitfalls = sol.get('pitfalls', []) if sol else []
    err_ref = extract_sections(ref, '易错点', '常见错误')
    if pitfalls or err_ref:
        ep = ['## ⚠️ 易错点']
        if err_ref:
            ep.append(err_ref)
        for pp in pitfalls:
            ep.append(f'- {pp}')
        parts.append('\n\n'.join(ep))

    # 复杂度（参考）
    comp = extract_sections(ref, '复杂度')
    if comp:
        parts.append('## 📊 复杂度分析\n\n' + comp)

    # 实际业务应用
    biz = extract_sections(ref, '业务应用', '实际业务')
    if biz:
        parts.append('## 🏢 实际业务应用\n\n' + biz)

    # 名著类比 / 森林故事
    story = extract_sections(ref, '名著', '情节类比')
    forest = extract_sections(ref, '森林', '小故事')
    analogy_parts = []
    if story: analogy_parts.append(story)
    if forest: analogy_parts.append(forest)
    if analogy_parts:
        parts.append('## 📖 形象类比\n\n' + '\n\n'.join(analogy_parts))

    # 记忆口诀
    memo = extract_sections(ref, '记忆', '口诀')
    if memo:
        parts.append('## 🎵 记忆口诀\n\n' + memo)

    # 延伸练习
    ext = extract_sections(ref, '延伸', '扩展', '练习')
    if ext:
        parts.append('## 🔗 延伸练习\n\n' + ext)

    return '\n\n'.join(parts)


def main():
    problems = parse_problems()
    sols = parse_solutions()
    print(f'parsed {len(problems)} problems, {len(sols)} solutions')

    # 检查参考覆盖
    ref_count = sum(1 for p in problems if parse_reference(p['id']) is not None)
    print(f'reference coverage: {ref_count}/{len(problems)}')

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
        ref = parse_reference(p['id'])
        body = build_body(p, sol, ref)
        thinking = sol.get('thinking', '') if sol else ''

        tags_lines = '\n'.join(f'  - "{yaml_esc(t)}"' for t in p['tags']) if p['tags'] else '  []'
        feynman_essence = yaml_esc(thinking[:100]) if thinking else ''
        # 从参考思考路径取 essence
        if ref:
            for key, val in ref.items():
                if '题意翻译' in key:
                    feynman_essence = yaml_esc(val[:100])
                    break

        fm = ['---']
        fm.append(f'id: "{int(p["id"]):04d}"')
        fm.append(f'slug: "{p["slug"]}"')
        fm.append(f'lcId: {p["id"]}')
        fm.append(f'title: "{yaml_esc(p["title"])}"')
        fm.append(f'difficulty: "{p["diff"]}"')
        fm.append(f'category: "{cat_dir}"')
        fm.append('tags:')
        fm.append(tags_lines)
        fm.append(f'url: "{p["url"]}"')
        fm.append(f'planOrder: {order}')
        fm.append(f'hasViz: true')
        fm.append(f'hasDiagram: {"true" if p["id"] in DIAGRAM_IDS else "false"}')
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
        fm.append(f'# {p["id"]}. {p["title"]}\n')
        fm.append(f'> 难度：**{p["diff"]}** | 分类：{p["cat"]} | 标签：{", ".join(p["tags"])}\n')
        fm.append(f'> 🔗 力扣链接：[{p["url"]}]({p["url"]})\n')
        fm.append(body + '\n')

        open(path, 'w', encoding='utf-8').write('\n'.join(fm))
        total += 1

    print(f'rewrote {total} questions to {OUT}')


if __name__ == '__main__':
    main()
