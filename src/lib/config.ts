import type { Algorithm } from './types';

export interface CategoryConfig {
  label: string;
  icon: string;
  color: string;
}

export const APP_CONFIG = {
  appName: '算法面试题库',
  appNameShort: '算法面试',
  appIcon: '🧮',
  appVersion: '3.0',
  storagePrefix: 'algo-interview',
  githubUrl: 'https://sunarthur86.github.io/algorithm-interview/',
  repoUrl: 'https://github.com/SunArthur86/algorithm-interview',
  themeColor: '#f97316',
  categories: {
    'all': { label: '全部', icon: '📚', color: '#f97316' },
    'hash': { label: '哈希', icon: '#️⃣', color: '#ef4444' },
    'two-pointers': { label: '双指针', icon: '🔀', color: '#f97316' },
    'sliding-window': { label: '滑动窗口', icon: '🪟', color: '#eab308' },
    'substring': { label: '子串', icon: '🔗', color: '#84cc16' },
    'array': { label: '普通数组', icon: '📊', color: '#22c55e' },
    'matrix': { label: '矩阵', icon: '🔲', color: '#14b8a6' },
    'linked-list': { label: '链表', icon: '⛓️', color: '#06b6d4' },
    'binary-tree': { label: '二叉树', icon: '🌳', color: '#3b82f6' },
    'graph': { label: '图论', icon: '🕸️', color: '#6366f1' },
    'backtracking': { label: '回溯', icon: '↩️', color: '#8b5cf6' },
    'binary-search': { label: '二分查找', icon: '🔍', color: '#a855f7' },
    'stack': { label: '栈', icon: '🥞', color: '#d946ef' },
    'heap': { label: '堆', icon: '⛰️', color: '#ec4899' },
    'greedy': { label: '贪心算法', icon: '🎯', color: '#f43f5e' },
    'dynamic-programming': { label: '动态规划', icon: '🧩', color: '#0ea5e9' },
    'multi-dp': { label: '多维动态规划', icon: '🧊', color: '#64748b' },
    'techniques': { label: '技巧', icon: '⚡', color: '#facc15' },
  } as Record<string, CategoryConfig>,
  columnSources: {
    'data-structure-beauty': { label: '数据结构与算法之美', icon: '📘' },
    'dynamic-programming': { label: '动态规划面试宝典', icon: '📗' },
    'labuladong': { label: 'labuladong 算法小抄', icon: '📕' },
  } as Record<string, { label: string; icon: string }>,
  aboutText:
    'LeetCode 热题 100 完整 Java 题解 + 逐题动画 + 知识专栏 + 智能复习。',
} as const;

export const ALGO_LABELS: Record<Algorithm, string> = {
  sm2: 'SM-2 智能间隔',
  leitner: 'Leitner 卡盒',
  ebbinghaus: '艾宾浩斯曲线',
};
