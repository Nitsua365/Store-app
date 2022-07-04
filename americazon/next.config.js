/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    REDIS_URL: process.env.REDIS_URL,
    LOCAL_API: process.env.LOCAL_API,
  },
  images: {
    domains: ['m.media-amazon.com']
  }
}

module.exports = nextConfig
