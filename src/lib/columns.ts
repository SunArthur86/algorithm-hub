import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import type { Column } from './types';

const COLUMNS_DIR = path.join(process.cwd(), 'columns');

function loadAll(): Column[] {
  if (!fs.existsSync(COLUMNS_DIR)) return [];
  const out: Column[] = [];
  for (const source of fs.readdirSync(COLUMNS_DIR).sort()) {
    const srcDir = path.join(COLUMNS_DIR, source);
    if (!fs.statSync(srcDir).isDirectory()) continue;
    for (const file of fs.readdirSync(srcDir).filter((f) => f.endsWith('.md')).sort()) {
      const raw = fs.readFileSync(path.join(srcDir, file), 'utf-8');
      const { data, content } = matter(raw);
      out.push({
        slug: String(data.slug || file.replace(/\.md$/, '')),
        title: String(data.title || ''),
        source,
        chapter: String(data.chapter || ''),
        order: Number(data.order || 0),
        related: Array.isArray(data.related) ? data.related.map(Number) : [],
        content: content.trim(),
      });
    }
  }
  return out;
}

let _cache: Column[] | null = null;

export function getAllColumns(): Column[] {
  if (_cache) return _cache;
  _cache = loadAll();
  return _cache;
}

export function getColumnBySlug(slug: string): Column | undefined {
  return getAllColumns().find((c) => c.slug === slug);
}
