'use client';

import { useEffect, useRef, useState } from 'react';

declare global {
  interface Window {
    VizEngine?: any;
    VIZ_TRACES?: any;
  }
}

const BASE = process.env.NODE_ENV === 'production' ? '/algorithm-interview' : '';

const SCRIPTS = [
  '/legacy/viz-engine.js',
  '/legacy/viz-traces-01.js',
  '/legacy/viz-traces-02.js',
  '/legacy/viz-traces-03.js',
  '/legacy/viz-traces-04.js',
  '/legacy/viz-traces-05.js',
  '/legacy/viz-traces-06.js',
];

let _scriptsLoaded: Promise<void> | null = null;

function loadAllScripts(): Promise<void> {
  if (_scriptsLoaded) return _scriptsLoaded;
  _scriptsLoaded = (async () => {
    for (const s of SCRIPTS) {
      await new Promise<void>((resolve, reject) => {
        const el = document.createElement('script');
        el.src = BASE + s;
        el.onload = () => resolve();
        el.onerror = () => reject(new Error('failed to load ' + s));
        document.body.appendChild(el);
      }).catch((e) => console.error(e));
    }
  })();
  return _scriptsLoaded;
}

export default function VizPlayer({ lcId }: { lcId: number }) {
  const [status, setStatus] = useState<'loading' | 'ready' | 'no-trace'>('loading');
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let cancelled = false;
    const key = String(lcId);

    (async () => {
      await loadAllScripts();
      if (cancelled || !containerRef.current) return;
      if (!window.VizEngine) {
        setStatus('no-trace');
        return;
      }
      // 重置初始化标志，强制重新绑定 DOM（每次挂载新 canvas）
      window.VizEngine._initialized = false;
      window.VizEngine.stop && window.VizEngine.stop();
      window.VizEngine.init();
      window.VizEngine._initialized = true;
      const has = window.VizEngine.load(key);
      if (cancelled) return;
      setStatus(has ? 'ready' : 'no-trace');
    })();

    return () => {
      cancelled = true;
      try {
        window.VizEngine?.stop?.();
      } catch {}
    };
  }, [lcId]);

  // 始终渲染完整的 DOM 骨架（canvas + 控件 + 状态元素），viz-engine 的 init() 才能 getElementById 命中
  return (
    <div ref={containerRef} style={{ marginTop: '12px' }}>
      <canvas
        id="viz-canvas"
        width={640}
        height={320}
        style={{
          width: '100%',
          maxWidth: 640,
          background: 'var(--card-secondary)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border)',
        }}
      />
      {/* viz-engine render() 会写这些元素 */}
      <div id="viz-message" style={{ textAlign: 'center', fontSize: '12px', color: 'var(--text-secondary)', margin: '6px 0', minHeight: '16px' }} />
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', justifyContent: 'center' }}>
        <button id="viz-step-back" style={btn}>◀</button>
        <button id="viz-play" style={{ ...btn, background: 'var(--primary)', color: '#fff', borderColor: 'var(--primary)' }}>▶ 播放</button>
        <button id="viz-step-fwd" style={btn}>▶|</button>
        <button id="viz-reset" style={btn}>↺</button>
        <input id="viz-speed" type="range" min={1} max={10} defaultValue={6} style={{ marginLeft: '6px', width: '100px' }} />
        <span id="viz-speed-val" style={{ fontSize: '12px', color: 'var(--text-tertiary)' }}>6</span>
      </div>
      <div style={{ marginTop: '6px' }}>
        <div id="viz-counter" style={{ textAlign: 'center', fontSize: '11px', color: 'var(--text-tertiary)' }} />
        <div id="viz-progress" style={{ height: '4px', background: 'var(--border)', borderRadius: '2px', marginTop: '4px', overflow: 'hidden' }} />
      </div>
      {status === 'loading' && (
        <div style={{ textAlign: 'center', padding: '8px', color: 'var(--text-tertiary)', fontSize: '12px' }}>
          加载动画引擎…
        </div>
      )}
      {status === 'no-trace' && (
        <p style={{ textAlign: 'center', fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '6px' }}>
          此题暂无逐题动画
        </p>
      )}
    </div>
  );
}

const btn: React.CSSProperties = {
  padding: '4px 12px',
  borderRadius: 'var(--radius-sm)',
  border: '1px solid var(--border)',
  background: 'var(--bg-soft)',
  color: 'var(--text)',
  cursor: 'pointer',
  fontSize: '13px',
};
