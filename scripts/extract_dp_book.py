#!/usr/bin/env python3
"""解析 156-动态规划面试宝典.epub → columns/dynamic-programming/*.md"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _epub_common import extract_epub

EPUB = '/Users/sunqingguang/Downloads/02.interview/算法/156-动态规划面试宝典.epub'
OUT = os.path.join(os.path.dirname(__file__), '..', 'columns', 'dynamic-programming')

if __name__ == '__main__':
    extract_epub(EPUB, 'dynamic-programming', OUT)
