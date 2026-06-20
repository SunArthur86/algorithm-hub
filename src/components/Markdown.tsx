'use client';

import { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';

// 自定义 img：原生 loading="lazy" + decoding="async"，首屏外的图延迟加载
function LazyImg({ src, alt }: { src?: string; alt?: string }) {
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={src}
      alt={alt || ''}
      loading="lazy"
      decoding="async"
      style={{ maxWidth: '100%', height: 'auto', borderRadius: 'var(--radius-md)', margin: '8px 0' }}
    />
  );
}

export default function Markdown({ children }: { children: string }) {
  // 缓存渲染结果（题解内容不变时避免重复 parse）
  const content = useMemo(
    () => (
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{ img: LazyImg as any }}
      >
        {children}
      </ReactMarkdown>
    ),
    [children]
  );
  return (
    <div className="prose max-w-none" style={{ fontSize: '14px', color: 'var(--text)' }}>
      {content}
    </div>
  );
}
