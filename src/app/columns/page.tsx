import { getAllColumns } from '@/lib/columns';
import { APP_CONFIG } from '@/lib/config';
import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: '算法知识专栏 - 算法面试',
  description: '数据结构与算法之美、动态规划面试宝典、labuladong 算法小抄 三本书的知识专栏。',
};

export default function Page() {
  const columns = getAllColumns();
  const bySource: Record<string, typeof columns> = {};
  for (const c of columns) (bySource[c.source] ||= []).push(c);

  return (
    <main style={{ maxWidth: 760, margin: '0 auto', padding: '16px', minHeight: '100vh' }}>
      <Link href="/" style={{ display: 'inline-block', marginBottom: '12px', fontSize: '13px' }}>
        ← 返回题库
      </Link>
      <h1 style={{ fontSize: '22px', fontWeight: 700, margin: '0 0 4px' }}>📚 算法知识专栏</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: '13px', margin: '0 0 20px' }}>
        共 {columns.length} 篇，来自三本经典算法书籍。
      </p>

      {Object.entries(bySource).map(([src, cols]) => {
        const cfg = APP_CONFIG.columnSources[src] || { label: src, icon: '📄' };
        return (
          <section key={src} style={{ marginBottom: '28px' }}>
            <h2 style={{ fontSize: '17px', fontWeight: 600, margin: '0 0 10px' }}>
              {cfg.icon} {cfg.label}{' '}
              <span style={{ fontSize: '12px', color: 'var(--text-tertiary)', fontWeight: 400 }}>
                ({cols.length})
              </span>
            </h2>
            <ol style={{ margin: 0, paddingLeft: '20px', lineHeight: 1.9 }}>
              {cols.map((c) => (
                <li key={c.slug} style={{ fontSize: '14px' }}>
                  <Link href={`/columns/${c.slug}/`}>{c.title}</Link>
                </li>
              ))}
            </ol>
          </section>
        );
      })}
      {columns.length === 0 && (
        <p style={{ color: 'var(--text-tertiary)', padding: '40px', textAlign: 'center' }}>
          暂无专栏。运行 scripts/extract_*.py 生成。
        </p>
      )}
    </main>
  );
}
