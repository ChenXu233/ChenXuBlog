# 构建阶段 —— 只在 CI runner 上执行（服务器 pull 到的镜像无此层）
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# 运行时阶段 —— 服务器只运行此层，零编译
FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/.output ./output

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000
ENV NUXT_API_INTERNAL_URL=http://backend:8000

EXPOSE 3000

CMD ["node", "output/server/index.mjs"]
