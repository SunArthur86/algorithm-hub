import { getTop100Plan } from '@/lib/study-plan';
import { getAllQuestions } from '@/lib/questions';
import StudyPlan from '@/components/StudyPlan';
import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'LeetCode 热题 100 学习计划 - 算法面试',
  description: '复刻 leetcode.cn/studyplan/top-100-liked，按 17 分类顺序刷题，进度本地保存。',
};

export default function Page() {
  const plan = getTop100Plan();
  const questions = getAllQuestions();
  return (
    <main style={{ maxWidth: 760, margin: '0 auto', padding: '16px', minHeight: '100vh' }}>
      <Link href="/" style={{ display: 'inline-block', marginBottom: '12px', fontSize: '13px' }}>
        ← 返回题库
      </Link>
      <StudyPlan plan={plan} questions={questions} />
    </main>
  );
}
