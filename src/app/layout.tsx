import './globals.css';

export const metadata = {
  title: '算法面试题库',
  description: 'LeetCode 热题 100 题解、逐题动画、知识专栏与智能复习',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh">
      <body>{children}</body>
    </html>
  );
}
