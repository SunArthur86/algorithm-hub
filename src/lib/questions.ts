import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import type { Question } from './types';

const QUESTIONS_DIR = path.join(process.cwd(), 'questions');

function loadAll(): Question[] {
  if (!fs.existsSync(QUESTIONS_DIR)) return [];
  const out: Question[] = [];
  const catDirs = fs.readdirSync(QUESTIONS_DIR).sort();
  for (const catDir of catDirs) {
    const full = path.join(QUESTIONS_DIR, catDir);
    if (!fs.statSync(full).isDirectory()) continue;
    const files = fs.readdirSync(full).filter((f) => f.endsWith('.md')).sort();
    for (const file of files) {
      const raw = fs.readFileSync(path.join(full, file), 'utf-8');
      const { data, content } = matter(raw);
      const title = String(data.title || '');
      out.push({
        id: String(data.id || file.replace(/\.md$/, '')),
        lcId: Number(data.lcId || 0),
        slug: String(data.slug || ''),
        title,
        question: title, // 兼容 java-interview 组件用法
        answer: content.trim(),
        difficulty: String(data.difficulty || 'Medium'),
        category: String(data.category || catDir),
        categories: [String(data.category || catDir)],
        tags: Array.isArray(data.tags) ? data.tags.map(String) : [],
        url: String(data.url || ''),
        planOrder: Number(data.planOrder || 0),
        hasViz: !!data.hasViz,
        hasDiagram: !!data.hasDiagram,
        feynman: data.feynman || undefined,
        first_principle: data.first_principle || undefined,
      });
    }
  }
  return out;
}

let _cache: Question[] | null = null;

export function getAllQuestions(): Question[] {
  if (_cache) return _cache;
  _cache = loadAll();
  return _cache;
}

export function getQuestionByLcId(lcId: string): Question | undefined {
  return getAllQuestions().find((q) => String(q.lcId) === String(lcId));
}

export function getAllLcIds(): string[] {
  return getAllQuestions().map((q) => String(q.lcId));
}
