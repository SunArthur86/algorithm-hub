#!/usr/bin/env python3
"""压缩 labuladong 图片：PNG → WebP (q=85，视觉无损)，并更新专栏 markdown 引用。

策略：
- 用 cwebp -q 85（保持清晰度，体积约缩小 70-85%）
- 同名 .webp 输出到同目录
- 扫描 columns/labuladong/*.md，把图片引用替换为 .webp
- 删除原 .png（可选，默认删除以释放体积）
"""
import os
import re
import glob
import subprocess

IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'columns', 'labuladong')
MD_DIR = os.path.join(os.path.dirname(__file__), '..', 'columns', 'labuladong')
KEEP_PNG = os.environ.get('KEEP_PNG', '0') == '1'


def main():
    pngs = sorted(glob.glob(os.path.join(IMG_DIR, '*.png')))
    print(f'compressing {len(pngs)} images → webp (q=85)')
    before = 0
    after = 0
    for i, png in enumerate(pngs):
        webp = png[:-4] + '.webp'
        before += os.path.getsize(png)
        # cwebp -q 85；若宽度>1600，按比例缩到 1600（清晰度足够，进一步省体积）
        cmd = ['cwebp', '-quiet', '-q', '85', png, '-o', webp]
        # 大图缩小到最大宽度 1600（保持清晰度）
        try:
            from PIL import Image
            with Image.open(png) as im:
                w, h = im.size
            if w > 1600:
                cmd = ['cwebp', '-quiet', '-q', '85', '-resize', '1600', '0', png, '-o', webp]
        except Exception:
            pass
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            after += os.path.getsize(webp)
            if not KEEP_PNG:
                os.remove(png)
        except subprocess.CalledProcessError as e:
            print(f'  ERR {os.path.basename(png)}: {e.stderr.decode("utf-8", "ignore")[:100]}')
        if (i + 1) % 100 == 0:
            print(f'  …{i + 1}/{len(pngs)} done')
    print(f'size: {before / 1024 / 1024:.1f}MB → {after / 1024 / 1024:.1f}MB '
          f'({(1 - after / before) * 100:.0f}% smaller)')

    # 更新 markdown 中的图片引用
    print('updating markdown image references…')
    md_files = glob.glob(os.path.join(MD_DIR, '*.md'))
    ref_count = 0
    for md in md_files:
        raw = open(md, encoding='utf-8').read()
        # 匹配 ![alt](path.png) 形式，把 .png 改 .webp
        new = re.sub(r'(\!\[[^\]]*\]\([^)]*?)\.png\)', r'\1.webp)', raw)
        # 也处理裸 .png 引用（非 markdown 图片语法的）
        if new != raw:
            open(md, 'w', encoding='utf-8').write(new)
            ref_count += 1
    print(f'updated {ref_count} markdown files')


if __name__ == '__main__':
    main()
