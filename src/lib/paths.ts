/**
 * basePath 辅助：所有手写绝对 URL（<a href>、window.location、脚本路径）
 * 都需手动拼接 basePath，否则生产环境（/algorithm-interview/）会 404。
 * 客户端组件内部跳转请优先用 next/link 的 <Link>，它会自动处理 basePath。
 */
export const BASE_PATH = process.env.NODE_ENV === 'production' ? '/algorithm-interview' : '';

/** 把以 / 开头的路径补上 basePath。 */
export function withBase(p: string): string {
  if (!p.startsWith('/')) return p;
  return BASE_PATH + p;
}
