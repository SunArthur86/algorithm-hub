#!/usr/bin/env python3
"""解析 01-数据结构与算法之美.epub → columns/data-structure-beauty/*.md"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _epub_common import extract_epub

EPUB = '/Users/sunqingguang/Downloads/02.interview/算法/01-数据结构与算法之美.epub'
OUT = os.path.join(os.path.dirname(__file__), '..', 'columns', 'data-structure-beauty')

if __name__ == '__main__':
    extract_epub(EPUB, 'data-structure-beauty', OUT)
