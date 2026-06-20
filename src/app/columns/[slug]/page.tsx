import { getAllColumns, getColumnBySlug } from '@/lib/columns';
import { getAllQuestions } from '@/lib/questions';
import { APP_CONFIG } from '@/lib/config';
import Markdown from '@/components/Markdown';
import { notFound } from 'next/navigation';
import type { Metadata } from 'next';

export function generateStaticParams() {
  return getAllColumns().map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const c = getColumnBySlug(slug);
  return { title: c ? `${c.title} - 算法面试` : '算法面试' };
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const c = getColumnBySlug(slug);
  if (!c) notFound();
  const questions = getAllQuestions();
  const related = c.related
    .map((id) => questions.find((q) => q.lcId === id))
    .filter((q): q is NonNullable<typeof q> => !!q);
  const srcCfg = APP_CONFIG.columnSources[c.source];

  return (
    <main style={{ maxWidth: 760, margin: '0 auto', padding: '16px', minHeight: '100vh' }}>
      <a href="/columns/" style={{ display: 'inline-block', marginBottom: '12px', fontSize: '13px' }}>
        ← 返回专栏
      </a>
      <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginBottom: '4px' }}>
        {srcCfg?.icon} {srcCfg?.label}
      </div>
      <h1 style={{ fontSize: '22px', fontWeight: 700, margin: '0 0 16px' }}>{c.title}</h1>
      <Markdown>{c.content}</Markdown>

      {related.length > 0 && (
        <section style={{ marginTop: '24px', padding: '16px', background: 'var(--card-secondary)', borderRadius: 'var(--radius-md)' }}>
          <h2 style={{ fontSize: '15px', fontWeight: 600, margin: '0 0 8px' }}>🔗 相关热题 100</h2>
          <ul style={{ margin: 0, paddingLeft: '20px', lineHeight: 1.8 }}>
            {related.map((q) => (
              <li key={q.lcId} style={{ fontSize: '13px' }}>
                <a href={`/question/${q.lcId}/`}>
                  #{q.lcId} {q.title}
                </a>
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
