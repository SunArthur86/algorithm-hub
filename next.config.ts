import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? '/algorithm-interview' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/algorithm-interview/' : undefined,
  trailingSlash: true,
  images: { unoptimized: true },
};

export default nextConfig;
