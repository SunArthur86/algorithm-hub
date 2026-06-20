'use client';

import { useMemo } from 'react';
import Link from 'next/link';
import type { Question } from '@/lib/types';
import type { StudyPlan as Plan } from '@/lib/study-plan';
import { useStore } from '@/lib/store';
import { APP_CONFIG } from '@/lib/config';
import ProgressRing from './ProgressRing';

const DIFF_COLOR: Record<string, string> = {
  Easy: 'var(--diff-easy)',
  Medium: 'var(--diff-medium)',
  Hard: 'var(--diff-hard)',
};

interface Props {
  plan: Plan;
  questions: Question[];
}

export default function StudyPlan({ plan, questions }: Props) {
  const planProgress = useStore((s) => s.planProgress);
  const togglePlanDone = useStore((s) => s.togglePlanDone);
  const logStudy = useStore((s) => s.logStudy);
  const streak = useStore((s) => s.streak);
  const dailyGoal = useStore((s) => s.dailyGoal);

  // lcId -> question
  const byLc = useMemo(() => {
    const m = new Map<number, Question>();
    for (const q of questions) m.set(q.lcId, q);
    return m;
  }, [questions]);

  const allLcIds = useMemo(() => plan.groups.flatMap((g) => g.lcIds), [plan]);
  const doneCount = useMemo(
    () => allLcIds.filter((id) => planProgress[String(id)]).length,
    [allLcIds, planProgress]
  );
  const total = allLcIds.length;
  const remaining = total - doneCount;
  const etaDays = dailyGoal > 0 ? Math.ceil(remaining / dailyGoal) : 0;
  const etaDate = useMemo(() => {
    const d = new Date();
    d.setDate(d.getDate() + etaDays);
    return d.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' });
  }, [etaDays]);

  return (
    <div>
      {/* 概览 */}
      <section
        style={{
          display: 'flex',
          gap: '20px',
          alignItems: 'center',
          background: 'var(--card)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-lg)',
          padding: '20px 24px',
          marginBottom: '20px',
          flexWrap: 'wrap',
        }}
      >
        <ProgressRing value={doneCount / total} done={doneCount} total={total} size={110} label="完成" />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1, minWidth: 220 }}>
          <h1 style={{ fontSize: '20px', fontWeight: 700, margin: 0 }}>{plan.title}</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', margin: 0 }}>{plan.subtitle}</p>
          <div style={{ display: 'flex', gap: '16px', fontSize: '13px', flexWrap: 'wrap' }}>
            <span>🔥 连续学习 <strong>{streak}</strong> 天</span>
            <span>✅ 已完成 <strong>{doneCount}</strong>/{total}</span>
            <span>⏳ 剩余 <strong>{remaining}</strong> 题</span>
            <span>📅 预计 <strong>{remaining === 0 ? '已完成 🎉' : `${etaDate}（${etaDays}天）`}</strong></span>
          </div>
        </div>
      </section>

      {/* 分组列表 */}
      {plan.groups.map((g, gi) => {
        const gDone = g.lcIds.filter((id) => planProgress[String(id)]).length;
        return (
          <section key={gi} style={{ marginBottom: '20px' }}>
            <h2
              style={{
                fontSize: '15px',
                fontWeight: 600,
                margin: '0 0 8px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
              }}
            >
              <span
                style={{
                  fontSize: '11px',
                  padding: '2px 8px',
                  borderRadius: '999px',
                  background: 'var(--primary-soft)',
                  color: 'var(--primary)',
                }}
              >
                {gDone}/{g.lcIds.length}
              </span>
              {g.name}
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {g.lcIds.map((lcId) => {
                const q = byLc.get(lcId);
                const done = !!planProgress[String(lcId)];
                if (!q) {
                  return (
                    <div key={lcId} style={row(done)}>
                      <input type="checkbox" checked={done} readOnly style={{ accentColor: 'var(--primary)' }} />
                      <span style={{ fontFamily: 'monospace', fontSize: '12px', color: 'var(--text-tertiary)' }}>#{lcId}</span>
                      <span style={{ color: 'var(--text-tertiary)' }}>(未导入)</span>
                    </div>
                  );
                }
                return (
                  <Link key={lcId} href={`/question/${lcId}/`} style={{ ...row(done), textDecoration: 'none', color: 'var(--text)' }}>
                    <input
                      type="checkbox"
                      checked={done}
                      onClick={(e) => {
                        e.preventDefault();
                        togglePlanDone(String(lcId));
                        logStudy('know', undefined);
                      }}
                      style={{ accentColor: 'var(--primary)' }}
                    />
                    <span style={{ fontFamily: 'monospace', fontSize: '12px', color: 'var(--text-tertiary)', minWidth: 44 }}>#{lcId}</span>
                    <span style={{ flex: 1, color: done ? 'var(--text-tertiary)' : 'var(--text)', textDecoration: done ? 'line-through' : 'none' }}>
                      {q.title}
                    </span>
                    <span
                      style={{
                        fontSize: '10px',
                        fontWeight: 600,
                        padding: '1px 6px',
                        borderRadius: '4px',
                        color: '#fff',
                        background: DIFF_COLOR[q.difficulty] || 'var(--text-tertiary)',
                      }}
                    >
                      {q.difficulty}
                    </span>
                    {(APP_CONFIG as any) && q.hasViz && <span title="逐题动画">🎬</span>}
                  </Link>
                );
              })}
            </div>
          </section>
        );
      })}
    </div>
  );
}

function row(done: boolean): React.CSSProperties {
  return {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '8px 12px',
    borderRadius: 'var(--radius-sm)',
    background: done ? 'var(--card-secondary)' : 'var(--card)',
    border: '1px solid var(--border)',
    fontSize: '13px',
  };
}
