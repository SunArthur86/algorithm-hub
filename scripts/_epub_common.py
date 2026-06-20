#!/usr/bin/env python3
"""共享：epub/html → markdown 转换 + 顺序 ASCII slug（dsb-001 / dp-001）。

被 extract_ds_beauty.py / extract_dp_book.py 复用。
"""
import os
import re
from bs4 import BeautifulSoup

SKIP_TITLE_KEYWORDS = [
    '版权', '目录', '前言', '封底', '封面', '关于本书',
    '内容简介', '作者简介', '勘误', '参考文献', '致谢',
]

SOURCE_PREFIX = {
    'data-structure-beauty': 'dsb',
    'dynamic-programming': 'dp',
}


def html_to_markdown(soup):
    """章节正文（h2-h4 / p / pre / li / blockquote）→ 简化 markdown。"""
    lines = []
    body = soup.find('body') or soup
    for el in body.find_all(['h2', 'h3', 'h4', 'p', 'pre', 'li', 'blockquote']):
        if el.name == 'li' and el.find('p'):
            continue
        text = el.get_text('\n', strip=True)
        if not text:
            continue
        if el.name == 'h2':
            lines.append(f'\n## {text}\n')
        elif el.name == 'h3':
            lines.append(f'\n### {text}\n')
        elif el.name == 'h4':
            lines.append(f'\n#### {text}\n')
        elif el.name == 'pre':
            lines.append(f'\n```\n{text}\n```\n')
        elif el.name == 'li':
            lines.append(f'- {text}')
        elif el.name == 'blockquote':
            lines.append(f'\n> {text}\n')
        else:
            lines.append(text + '\n')
    return '\n'.join(lines).strip()


def yaml_escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')


def write_md(out_dir, source, order, title, content):
    prefix = SOURCE_PREFIX.get(source, source)
    slug = f'{prefix}-{order:03d}'
    md = (
        f'---\n'
        f'slug: "{slug}"\n'
        f'title: "{yaml_escape(title)}"\n'
        f'source: {source}\n'
        f'chapter: "{yaml_escape(title)}"\n'
        f'order: {order}\n'
        f'related: []\n'
        f'---\n\n'
        f'# {title}\n\n'
        f'{content}\n'
    )
    fname = f'{order:02d}.md'
    with open(os.path.join(out_dir, fname), 'w', encoding='utf-8') as f:
        f.write(md)


def extract_epub(epub_path, source, out_dir):
    """主提取流程：epub → columns/<source>/*.md（顺序 ASCII slug）。"""
    import zipfile
    os.makedirs(out_dir, exist_ok=True)
    zf = zipfile.ZipFile(epub_path)
    htmls = sorted(
        [n for n in zf.namelist() if re.match(r'OEBPS/Text/\d+\.html', n)],
        key=lambda n: int(re.search(r'(\d+)\.html', n).group(1)),
    )
    print(f'[{source}] found {len(htmls)} chapter html files')
    order = 0
    skipped = 0
    for name in htmls:
        raw = zf.read(name).decode('utf-8', 'ignore')
        soup = BeautifulSoup(raw, 'html.parser')
        heading = soup.find(['h1', 'h2', 'h3'])
        title = heading.get_text(strip=True) if heading else ''
        content = html_to_markdown(soup)
        if not title or len(content) < 300 or any(k in title for k in SKIP_TITLE_KEYWORDS):
            skipped += 1
            continue
        order += 1
        write_md(out_dir, source, order, title, content)
    print(f'[{source}] extracted {order} chapters, skipped {skipped}')
    return order
