# 纯运行时镜像 —— 无构建阶段！
# .output 由 CI 编译后随部署传入，服务器只 COPY 不编译
FROM node:22-alpine

WORKDIR /app

COPY .output ./output

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000
ENV NUXT_API_INTERNAL_URL=http://backend:8000

EXPOSE 3000

CMD ["node", "output/server/index.mjs"]
