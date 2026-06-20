export interface Feynman {
  essence?: string;
  analogy?: string;
  key_points?: string[];
}
export interface FirstPrinciple {
  problem?: string;
  axioms?: string[];
  rebuild?: string;
}
export interface Question {
  id: string;
  lcId: number;
  slug: string;
  title: string;
  question: string; // 兼容 java-interview 用法（等于 title）
  answer: string; // 正文 markdown
  difficulty: string; // Easy/Medium/Hard
  category: string; // 分类 slug
  categories: string[];
  tags: string[];
  url: string;
  planOrder: number;
  hasViz: boolean;
  hasDiagram: boolean;
  feynman?: Feynman;
  first_principle?: FirstPrinciple;
}

export interface Column {
  slug: string;
  title: string;
  source: string;
  chapter: string;
  order: number;
  related: number[];
  content: string;
}

export type Rating = 'know' | 'fuzzy' | 'dont';
export type Algorithm = 'sm2' | 'leitner' | 'ebbinghaus';

export interface ReviewItem {
  algo: Algorithm;
  ease: number;
  interval: number;
  reps: number;
  lapses: number;
  box: number;
  phase: number;
  nextDate: string;
  lastDate: string;
  createdAt: string;
  history: { d: string; q: number }[];
}
