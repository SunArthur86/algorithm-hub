#!/usr/bin/env python3
"""解析 Fucking-Algorithm.pdf (labuladong 算法小抄) → columns/labuladong/*.md

利用 PDF 内嵌 TOC 书签（82 条，1/2 级），按章节切分页面范围，
抽取文字 + 图片（图片存 public/columns/labuladong/）。
顺序 ASCII slug（lbd-001）。
"""
import os
import fitz  # PyMuPDF
from _epub_common import yaml_escape, SKIP_TITLE_KEYWORDS

PDF = '/Users/sunqingguang/Downloads/02.interview/算法/Fucking-Algorithm.pdf'
OUT_MD = os.path.join(os.path.dirname(__file__), '..', 'columns', 'labuladong')
OUT_IMG = os.path.join(os.path.dirname(__file__), '..', 'public', 'columns', 'labuladong')


def write_md(order, title, content):
    slug = f'lbd-{order:03d}'
    md = (
        f'---\n'
        f'slug: "{slug}"\n'
        f'title: "{yaml_escape(title)}"\n'
        f'source: labuladong\n'
        f'chapter: "{yaml_escape(title)}"\n'
        f'order: {order}\n'
        f'related: []\n'
        f'---\n\n'
        f'# {title}\n\n'
        f'{content}\n'
    )
    with open(os.path.join(OUT_MD, f'{order:02d}.md'), 'w', encoding='utf-8') as f:
        f.write(md)


def main():
    os.makedirs(OUT_MD, exist_ok=True)
    os.makedirs(OUT_IMG, exist_ok=True)
    doc = fitz.open(PDF)
    toc = doc.get_toc()
    print(f'pages: {doc.page_count}, toc entries: {len(toc)}')
    if not toc:
        print('ERROR: no TOC bookmarks found; aborting')
        return

    order = 0
    for i, (level, title, page) in enumerate(toc):
        if level > 2:
            continue
        if title.strip() in SKIP_TITLE_KEYWORDS:
            continue
        start = page - 1  # fitz 页码从 0 开始
        end = (toc[i + 1][2] - 1) + 1 if i + 1 < len(toc) else doc.page_count

        text_parts = []
        img_count = 0
        for pno in range(start, min(end, doc.page_count)):
            page_obj = doc[pno]
            text_parts.append(page_obj.get_text())
            for img_info in page_obj.get_images(full=True):
                xref = img_info[0]
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n - pix.alpha >= 4:  # CMYK -> RGB
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    if pix.width < 40 or pix.height < 40:
                        pix = None
                        continue
                    order_for_img = order + 1
                    img_name = f'{order_for_img:02d}-{img_count:02d}.png'
                    pix.save(os.path.join(OUT_IMG, img_name))
                    pix = None
                    img_count += 1
                except Exception as e:
                    print(f'  img extract warn (p{pno}): {e}')

        full = '\n'.join(text_parts).strip()
        if len(full) < 300:
            continue

        order += 1
        write_md(order, title, full)

    print(f'extracted {order} chapters; images in {OUT_IMG}')


if __name__ == '__main__':
    main()
