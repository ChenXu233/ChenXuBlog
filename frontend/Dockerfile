# 构建阶段
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json pnpm-lock.yaml* ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

# 运行阶段
FROM nginx:alpine
COPY --from=builder /app/dist /var/www/html
EXPOSE 80
