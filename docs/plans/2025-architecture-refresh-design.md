# ChenXuBlog 完整架构刷新设计

> 日期: 2025-08-06
> 目标: 前后端全量刷新，实现可落地的完整博客系统

---

## 一、整体架构

```
┌─ 浏览器 ──────────────────────────────────┐
│  Nuxt 3 SSR (页面渲染层)                   │
│  Nuxt UI v3 (Radix Vue + Tailwind v4)      │
│  SSR 首屏 / CSR 交互                       │
└──────────────┬─────────────────────────────┘
               │ HTTP (JSON API)
               ▼
┌─ Caddy 反向代理 ───────────────────────────┐
│  /apis/*     → FastAPI 后端                │
│  /images/*   → MinIO (代理或直连)          │
│  /*          → Nuxt (SSR/静态资源)         │
└──────────────┬─────────────────────────────┘
               │
┌─ FastAPI (Python 3.13+) ───────────────────┐
│  JWT 认证 / RBAC 权限                       │
│  文章 CRUD / 评论 / 用户                    │
│  SQLAlchemy 2.0 + SQLite / Alembic          │
│  S3 SDK → MinIO (图片上传/访问)            │
└─────────────────────┬───────────────────────┘
                      │
┌─────────────────────▼──────────────────────┐
│  MinIO (S3-compatible 对象存储)             │
│  Bucket: chenxu-blog-images                │
│  图片通过 presigned URL 或 Caddy 代理访问  │
└────────────────────────────────────────────┘
```

**铁律：**

- Nuxt 只做页面渲染，不碰数据库，不写业务逻辑
- FastAPI 是唯一的数据和权限边界
- 图片存储统一走 MinIO，本地文件系统只存代码
- 部署三容器（Nuxt + FastAPI + MinIO），Caddy 反代

---

## 二、后端设计（FastAPI）

### 2.1 目录结构

```
backend/
├── main.py                    # 入口
├── alembic.ini
├── migrations/
├── src/backend/
│   ├── __init__.py            # FastAPI app 创建 + lifespan
│   ├── config.py              # Pydantic Settings (含 MinIO 配置)
│   ├── database.py            # 引擎 + session
│   ├── logger.py              # Loguru 配置
│   ├── exceptions.py          # 统一异常处理器  ← 新增
│   ├── pagination.py          # 分页工具函数      ← 新增
│   ├── model/
│   │   ├── user.py            # User, Role, Permission, UserInfo
│   │   ├── blog.py            # Blog, Tag
│   │   ├── comment.py         # Comment
│   │   └── action.py          # Action (审计日志)
│   ├── schema/
│   │   ├── auth.py            # 登录/注册/重置密码
│   │   ├── user.py            # 用户信息
│   │   ├── blog.py            # 文章
│   │   ├── comment.py         # 评论
│   │   ├── permission.py      # 权限
│   │   └── admin.py           # 管理后台
│   ├── router/
│   │   ├── __init__.py        # 注册所有路由
│   │   ├── v1/
│   │   │   ├── auth.py        # 登录/注册/刷新/验证/重置密码
│   │   │   ├── blog.py        # 文章 CRUD + 点赞
│   │   │   ├── comment.py     # 评论 CRUD
│   │   │   ├── user.py        # 用户信息
│   │   │   ├── permission.py  # 权限查询
│   │   │   ├── img_bed.py     # 图床 (MinIO S3)  ← 重写
│   │   │   └── admin.py       # 管理后台
│   │   └── router_manager.py  # 删除
│   ├── service/
│   │   ├── email.py           # 邮件发送
│   │   └── storage.py         # MinIO S3 客户端     ← 新增
│   └── utils/
│       ├── jwt.py             # 生成/验证 JWT
│       ├── dependencies.py    # 公共依赖       ← 新增
│       └── permission/
│           ├── __init__.py
│           ├── manager.py     # PermissionManager
│           └── decorator.py   # require_permissions
└── tests/
```

### 2.2 后端修复清单

| #   | 问题                                            | 修复方案                                                      |
| --- | ----------------------------------------------- | ------------------------------------------------------------- |
| 1   | `get_db()` 自动 commit                          | 去掉 `commit()`，改为写操作显式 commit                        |
| 2   | 评论接口强制登录                                | 公开 `GET /comment/get/{blog_id}`，去掉 `require_permissions` |
| 3   | `RouterManager` 空壳                            | 直接 `app.include_router()`                                   |
| 4   | `/auth/register` 和 `/auth/login` 分属两 router | 合并到同一个 `auth.py`                                        |
| 5   | `/token/refresh` 和 `/auth/refresh` 两套        | 保留 `/auth/refresh`，删掉 `/token/refresh`                   |
| 6   | Token 用自定义 header                           | 改为 `Authorization: Bearer <token>`                          |
| 7   | 分页代码重复                                    | 提取 `Pagination` 工具类                                      |
| 8   | `BlogResponse.like` 和 `likes_count` 重复       | 去掉 `like` 字段                                              |
| 9   | 多对多表用 `Column()` 旧语法                    | 统一改为 `mapped_column()`                                    |
| 10  | `Tag.select()` 旧版                             | 改为 `select(Tag)`                                            |
| 11  | 无统一异常处理器                                | 添加 `@app.exception_handler`                                 |
| 12  | `user_id` 类型不一致                            | 统一用 `uuid: str` 暴露给前端                                 |

### 2.3 完整 API 清单

所有端点前缀：`/apis/v1`

#### 认证 `/auth`

| 方法 | 路径                    | 说明       | 认证          | 备注                              |
| ---- | ----------------------- | ---------- | ------------- | --------------------------------- |
| POST | `/auth/register`        | 注册       | -             | 发送验证邮件                      |
| GET  | `/auth/verify/{token}`  | 邮箱验证   | -             | 返回 HTML 页面                    |
| POST | `/auth/login`           | 登录       | -             | 返回 access_token + refresh_token |
| POST | `/auth/refresh`         | 刷新 token | Refresh Token | 从 cookie 取 refresh_token        |
| POST | `/auth/forgot-password` | 忘记密码   | -             | 发送重置邮件                      |
| POST | `/auth/reset-password`  | 重置密码   | -             | Token + 新密码                    |

#### 文章 `/blog`

| 方法   | 路径              | 说明                       | 认证 |
| ------ | ----------------- | -------------------------- | ---- |
| GET    | `/blog`           | 文章列表（分页+搜索+标签） | -    |
| GET    | `/blog/{id}`      | 文章详情                   | -    |
| POST   | `/blog`           | 创建文章                   | JWT  |
| PUT    | `/blog/{id}`      | 更新文章                   | JWT  |
| DELETE | `/blog/{id}`      | 删除文章                   | JWT  |
| POST   | `/blog/{id}/like` | 点赞/取消                  | JWT  |
| GET    | `/blog/{id}/like` | 点赞状态                   | -    |

#### 评论 `/comment`

| 方法   | 路径                    | 说明               | 认证 |
| ------ | ----------------------- | ------------------ | ---- |
| POST   | `/comment`              | 创建评论           | JWT  |
| GET    | `/comment/{blog_id}`    | 获取评论（含嵌套） | -    |
| DELETE | `/comment/{comment_id}` | 删除评论           | JWT  |
| PUT    | `/comment/{comment_id}` | 更新评论           | JWT  |

#### 用户 `/user`

| 方法 | 路径                     | 说明         | 认证 |
| ---- | ------------------------ | ------------ | ---- |
| GET  | `/user/info`             | 当前用户信息 | JWT  |
| GET  | `/user/info/{user_uuid}` | 指定用户信息 | -    |
| PUT  | `/user/info`             | 编辑资料     | JWT  |

#### 权限 `/permission`

| 方法 | 路径                | 说明                 | 认证 |
| ---- | ------------------- | -------------------- | ---- |
| GET  | `/permission`       | 获取当前用户权限列表 | JWT  |
| POST | `/permission/check` | 检查指定权限         | JWT  |

#### 图床 `/img_bed`

| 方法 | 路径              | 说明     | 认证 |
| ---- | ----------------- | -------- | ---- |
| POST | `/img_bed`        | 上传图片 | JWT  |
| GET  | `/img_bed/{hash}` | 获取图片 | -    |

#### 管理后台 `/admin`

| 方法   | 路径                        | 说明         | 认证  |
| ------ | --------------------------- | ------------ | ----- |
| GET    | `/admin/stats`              | 仪表盘统计   | Admin |
| GET    | `/admin/users`              | 用户列表     | Admin |
| PUT    | `/admin/users/{id}/role`    | 修改用户角色 | Admin |
| DELETE | `/admin/users/{id}`         | 删除用户     | Admin |
| GET    | `/admin/blogs`              | 文章管理列表 | Admin |
| PUT    | `/admin/blogs/{id}/publish` | 切换发布状态 | Admin |
| DELETE | `/admin/blogs/{id}`         | 删除文章     | Admin |
| GET    | `/admin/comments`           | 评论管理列表 | Admin |
| DELETE | `/admin/comments/{id}`      | 删除评论     | Admin |
| GET    | `/admin/roles`              | 角色列表     | Admin |

### 2.4 数据库模型（ERD）

```
┌─────────────────────────────────────────────────────────┐
│                        users                            │
├─────────────────────────────────────────────────────────┤
│ id (PK) │ uuid (UK) │ username (UK) │ email (UK)       │
│ password_hash │ is_verified │ verify_token │ verify_expiry│
│ created_at                                             │
└──────────┬──────────────────────────────────┬───────────┘
           │ 1:N                              │ 1:1
           ▼                                  ▼
┌──────────────────┐   ┌──────────────────────────────┐
│     blogs        │   │         user_info            │
├──────────────────┤   ├──────────────────────────────┤
│ id (PK)          │   │ id (PK)                      │
│ user_uuid (FK)   │   │ user_uuid (FK)               │
│ title            │   │ avatar │ gender │ birthday    │
│ body (Markdown)  │   │ location │ introduction      │
│ published        │   └──────────────────────────────┘
│ cover_url        │
│ view_count       │   ┌──────────────────────────────┐
│ created_at       │   │          tags                │
│ updated_at       │   ├──────────────────────────────┤
└────────┬─────────┘   │ id (PK) │ name (UK)         │
         │ 1:N         └──────────────────────────────┘
         ▼                    ──── Many-to-Many ────
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│    comments      │   │   blog_tags      │   │   blog_likes     │
├──────────────────┤   ├──────────────────┤   ├──────────────────┤
│ id (PK)          │   │ blog_id (FK)     │   │ blog_id (FK)     │
│ blog_id (FK)     │   │ tag_id (FK)      │   │ user_uuid (FK)   │
│ user_id (FK)     │   └──────────────────┘   └──────────────────┘
│ content          │
│ parent_id (FK)   │   ┌──────────────────────────────────────────┐
│ created_at       │   │    user_role / role_permission          │
│ updated_at       │   ├──────────────────────────────────────────┤
└──────────────────┘   │ 多对多中间表                            │
                       └──────────────────────────────────────────┘
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   permissions    │   │      roles       │   │     actions      │
├──────────────────┤   ├──────────────────┤   ├──────────────────┤
│ id (PK)          │   │ id (PK)          │   │ id (PK)          │
│ target │ action  │   │ name (UK)        │   │ target │ action  │
│ description      │   │ description      │   │ is_passed        │
└──────────────────┘   │ is_default       │   │ description      │
                       └──────────────────┘   │ error_message    │
                                              │ created_at       │
                                              └──────────────────┘
```

### 2.5 MinIO 对象存储集成

#### 2.5.1 架构

```
FastAPI (img_bed.py)
    │
    ├── POST /img_bed → upload_image()
    │   ├── 验证 JWT + 权限
    │   ├── 读取文件内容
    │   ├── 计算 SHA256 hash
    │   ├── 存入 MinIO (bucket: chenxu-blog-images)
    │   └── 返回 presigned URL 或 代理 URL
    │
    └── GET /img_bed/{hash} → get_image()
        ├── 从 MinIO 获取文件
        └── 返回 FileResponse (代理模式) 或 302 重定向到 presigned URL
```

#### 2.5.2 配置项

```python
# config.py 新增
class AppConfig(BaseSettings):
    # ... 现有配置 ...

    # MinIO 配置
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "chenxu-blog-images"
    MINIO_SECURE: bool = False
    MINIO_PUBLIC_URL: str = ""
    MINIO_USE_PRESIGNED: bool = False
```

#### 2.5.3 存储服务层

```python
# service/storage.py
from minio import Minio

class StorageService:
    def __init__(self, config):
        self.client = Minio(
            config.MINIO_ENDPOINT,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=config.MINIO_SECURE,
        )
        self.bucket = config.MINIO_BUCKET
        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    async def upload(self, file_data: bytes, content_type: str) -> str:
        file_hash = hashlib.sha256(file_data).hexdigest()
        ext = content_type.split("/")[-1] if "/" in content_type else "bin"
        object_name = f"{file_hash}.{ext}"
        self.client.put_object(
            self.bucket, object_name,
            io.BytesIO(file_data), len(file_data),
            content_type=content_type,
        )
        return self._get_url(object_name)

    def _get_url(self, object_name: str) -> str:
        return f"/images/{object_name}"  # 走 Caddy 代理

    async def get(self, object_name: str) -> bytes:
        response = self.client.get_object(self.bucket, object_name)
        return response.read()

storage_service = StorageService(CONFIG)
```

#### 2.5.4 图床路由重写

```python
@img_bed.post("/")
async def upload_image(image: UploadFile = File(...)):
    data = await image.read()
    url = await storage_service.upload(data, image.content_type or "application/octet-stream")
    return {"url": url}

@img_bed.get("/{object_name}")
async def get_image(object_name: str):
    data = await storage_service.get(object_name)
    content_type = guess_type(object_name)[0] or "application/octet-stream"
    return Response(content=data, media_type=content_type)
```

#### 2.5.5 Docker Compose

```yaml
services:
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"

volumes:
  minio_data:
```

#### 2.5.6 Caddy 代理

```
/images/* {
    reverse_proxy minio:9000 /chenxu-blog-images/{path}
}
```

#### 2.5.7 迁移脚本

```python
async def migrate_images_to_minio():
    import glob
    for path in glob.glob("data/images/*"):
        with open(path, "rb") as f:
            data = f.read()
        url = await storage_service.upload(data, "image/png")
        print(f"{path} → {url}")
```

---

## 三、前端设计（Nuxt 3 + Nuxt UI）

### 3.1 目录结构

```
frontend/
├── app.vue                    # 根组件
├── app.config.ts              # 运行时配置
├── nuxt.config.ts             # Nuxt 配置
├── pages/
│   ├── index.vue              # → 重定向到 /home
│   ├── home.vue               # 首页（含特效）
│   ├── login.vue
│   ├── register.vue
│   ├── article/
│   │   ├── index.vue          # 文章列表
│   │   ├── [id].vue           # 文章详情
│   │   ├── create.vue         # 写文章
│   │   └── edit/[id].vue      # 编辑文章
│   ├── user/
│   │   └── [id].vue           # 用户主页
│   ├── archive.vue
│   ├── friend.vue
│   ├── diary.vue
│   ├── warmos.vue
│   └── admin/
│       ├── index.vue          # 仪表盘
│       ├── users.vue          # 用户管理
│       ├── roles.vue          # 角色管理
│       ├── articles.vue       # 文章管理
│       └── comments.vue       # 评论管理
├── components/
│   ├── BlogCard.vue
│   ├── BlogList.vue
│   ├── CommentItem.vue
│   ├── CommentList.vue
│   ├── Footer.vue
│   ├── LoadingOverlay.vue
│   ├── MarkdownEditor.vue
│   ├── WarmOS/
│   │   ├── Apps/
│   │   │   ├── browser/index.vue
│   │   │   └── terminal/index.vue
│   │   ├── ContextMenu.vue
│   │   ├── DockBar.vue
│   │   ├── SystemPanel.vue
│   │   └── Window.vue
│   └── effects/
│       ├── BambooParallax.vue
│       ├── BlossomCanvas.vue
│       ├── MouseTrail.vue
│       ├── RainCanvas.vue
│       └── SunriseParallax.vue
├── composables/
│   ├── useAuth.ts             # 认证（合并 auth + token + permission）
│   ├── useToast.ts            # 通知（替代 Error.vue）
│   └── useEffects.ts          # 统一特效管理器（风力/滚动/动画循环）  ← 新增
├── types/
│   ├── article.ts
│   ├── comment.ts
│   └── user.ts
├── utils/
│   └── api.ts                 # $fetch 封装
├── middleware/
│   └── auth.ts                # 路由守卫
├── public/
│   ├── favicon.ico
│   └── img/
└── server/
    └── tsconfig.json
```

### 3.2 页面映射

| 现有 vue-router 路由 | Nuxt 页面文件                 | 状态           |
| -------------------- | ----------------------------- | -------------- |
| `/home`              | `pages/home.vue`              | 迁移，保留特效 |
| `/login`             | `pages/login.vue`             | 迁移，重写样式 |
| `/register`          | `pages/register.vue`          | 迁移，重写样式 |
| `/article`           | `pages/article/index.vue`     | 迁移           |
| `/article/:id`       | `pages/article/[id].vue`      | 迁移           |
| `/article/create`    | `pages/article/create.vue`    | 迁移           |
| `/article/edit/:id`  | `pages/article/edit/[id].vue` | 迁移           |
| `/user/:id`          | `pages/user/[id].vue`         | 迁移           |
| `/archive`           | `pages/archive.vue`           | 迁移           |
| `/friend`            | `pages/friend.vue`            | 迁移           |
| `/diary`             | `pages/diary.vue`             | 迁移           |
| `/warmos`            | `pages/warmos.vue`            | 迁移           |
| `/admin`             | `pages/admin/index.vue`       | 迁移，重写     |
| `/admin/users`       | `pages/admin/users.vue`       | 迁移，重写     |
| `/admin/roles`       | `pages/admin/roles.vue`       | 迁移，重写     |
| `/admin/articles`    | `pages/admin/articles.vue`    | 迁移，重写     |
| `/admin/comments`    | `pages/admin/comments.vue`    | 迁移，重写     |

### 3.3 技术替换

| 旧方案                    | 新方案                        | 说明                               |
| ------------------------- | ----------------------------- | ---------------------------------- |
| Vite + Vue 3              | Nuxt 3                        | SSR + 文件路由                     |
| Element Plus              | Nuxt UI v3                    | el-avatar 改为 `<img>`             |
| Font Awesome 4            | Nuxt UI 图标 (Heroicons)      | `<UIcon name="i-heroicons-..." />` |
| axios                     | `$fetch` / `useFetch`         | Nuxt 内置                          |
| vue-router 配置式         | 文件路由                      | 自动生成                           |
| Pinia Options API         | Pinia Setup Store             | 更简洁的类型安全                   |
| 手动 localStorage         | `pinia-plugin-persistedstate` | 自动持久化                         |
| `Error.vue` + `createApp` | `useToast()`                  | Nuxt UI 内置                       |
| `alert()` 弹窗            | `useToast()`                  | 统一通知                           |
| `style.css`               | Tailwind + Nuxt UI 主题       | 统一设计系统                       |

### 3.4 状态管理设计

三个旧 Store 合并为一个 `useAuth`：

```ts
// composables/useAuth.ts
export const useAuth = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const user = ref<User | null>(null)
  const permissions = ref<string[]>([])

  const isAuthenticated = computed(() => !!token.value)

  async function login(evidence: string, password: string) { ... }
  async function refreshAccessToken() { ... }
  async function fetchUserInfo() { ... }
  async function fetchPermissions() { ... }
  function hasPermission(code: string): boolean { ... }
  function logout() { ... }

  return { token, refreshToken, user, permissions, isAuthenticated, ... }
}, { persist: true })
```

### 3.5 API 请求层

```ts
// utils/api.ts
export const api = $fetch.create({
  baseURL: "/apis/v1",
  headers: { "Content-Type": "application/json" },
  onRequest({ options }) {
    const auth = useAuth();
    if (auth.token) {
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${auth.token}`,
      };
    }
  },
  onResponseError({ response }) {
    const toast = useToast();
    if (response.status === 401) {
      const auth = useAuth();
      auth.refreshAccessToken(); // 尝试刷新
    }
    toast.add({
      title: response._data?.detail || "请求失败",
      color: "error",
      icon: "i-heroicons-exclamation-circle",
    });
  },
});
```

### 3.6 路由守卫

```ts
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, _from) => {
  const auth = useAuth();

  // 需要登录的页面
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return navigateTo(`/login?redirect=${to.fullPath}`);
  }

  // 需要权限的页面
  if (
    to.meta.requiresPermission &&
    !auth.hasPermission(to.meta.requiresPermission as string)
  ) {
    const toast = useToast();
    toast.add({ title: "无权限访问", color: "warning" });
    return navigateTo("/home");
  }
});
```

---

## 四、UI 主题设计

### 4.1 配色方案

基于你首页的暖色调风格：

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  ui: {
    theme: {
      colors: {
        primary: "rose", // 樱花粉 #f4b3c2
        secondary: "emerald", // 竹绿
        neutral: "slate",
      },
    },
  },
});
```

| 用途                | 色系      | Hex     |
| ------------------- | --------- | ------- |
| 主色调（按钮/链接） | Rose      | #f4b3c2 |
| 辅色调（强调）      | Emerald   | #34d399 |
| 背景（浅色）        | Slate-50  | #f8fafc |
| 背景（深色）        | Slate-900 | #0f172a |
| 文字                | Slate-800 | #1e293b |
| 柔和文字            | Slate-400 | #94a3b8 |

### 4.2 组件替换

| 旧元素                                       | 新写法                                                               |
| -------------------------------------------- | -------------------------------------------------------------------- |
| `<el-avatar :size="32" />`                   | `<img class="w-8 h-8 rounded-full">`                                 |
| `<i class="fa fa-user"></i>`                 | `<UIcon name="i-heroicons-user" />`                                  |
| `Error.vue` 弹窗                             | `useToast().add({ title, color: 'error' })`                          |
| 确认对话框                                   | `useToast().add({ ... })` 或 `<UModal>`                              |
| `alert()`                                    | `useToast().add({ title, color: 'warning' })`                        |
| `style.css` CSS 变量（`--color-primary` 等） | 迁移到 `app.config.ts` design tokens，组件通过 `useAppConfig()` 读取 |
| `var(--color-primary)` 在 `<style>` 中的引用 | 替换为 Tailwind 类或 Nuxt UI 主题色                                  |

---

## 五、实施计划

### 阶段一：后端修复（1-2天）

任务列表：

1. 修复 `get_db()` 自动 commit
2. 公开评论 GET 接口
3. 合并 auth router / token router
4. 删除 `RouterManager`
5. 添加 `Pagination` 工具类
6. 改为 `Authorization: Bearer`
7. 添加统一异常处理器
8. 清理 Schema 重复字段
9. 统一 SQLAlchemy 2.0 语法

### 阶段一B：MinIO 图床集成（1天）

1. 添加 `minio` Python 依赖
2. 创建 `service/storage.py`（S3 客户端）
3. 重写 `router/v1/img_bed.py`（MinIO 上传/读取）
4. 配置 `config.py` 新增 MinIO 配置项
5. 配置 `docker-compose.yml` 新增 MinIO 服务
6. 配置 Caddyfile 新增 `/images/*` 代理
7. 编写一次性迁移脚本（`data/images/` → MinIO）

### 阶段二：Nuxt 前端搭建（3-4天）

1. 初始化 Nuxt 项目（在 `frontend/` 目录内）
2. 安装 Nuxt UI + 配置主题
3. 迁移 `pages/` 文件路由
4. 迁移 `components/`（WarmOS、特效等不动）
5. 重写 `composables/useAuth.ts`
6. 重写 `utils/api.ts`
7. 替换 Element Plus / font-awesome → Nuxt UI
8. 删除 `Error.vue`，改用 `useToast()`
9. 添加 `middleware/auth.ts`

### 阶段三：后端功能补全（2-3天）

1. 完善用户注册流程（邮箱验证）
2. 完善密码重置流程
3. 完善后台管理页面 API
4. 添加用户头像上传
5. 添加文章封面图管理
6. 添加站内搜索功能

### 阶段四：前端页面完善（2-3天）

1. 重写后台管理页面（仪表盘、用户、角色、文章、评论）
2. 完善文章详情页（目录导航、代码高亮）
3. 完善评论交互（嵌套回复 UI）
4. 添加 404/403/500 错误页面
5. SEO 优化（useHead、OG 标签、sitemap）

### 阶段四B：首页特效重写（3-4天）

1. 创建 `composables/useEffects.ts`（统一风力场 + 滚动 + 动画循环）
2. 重写 `BambooParallax.vue`（Canvas 2D 物理引擎：节点摇摆 + 贝塞尔曲线）
3. 重写 `RainCanvas.vue`（集成风场，雨滴随风偏转）
4. 重写 `BlossomCanvas.vue`（樱花飘落受风影响）
5. 新增竹叶飘零粒子系统
6. 新增竹声音频（Web Audio API，风/滚深度联动）
7. 新增雾效 + 景深感
8. 整合 `Home.vue` 所有特效，通过 `useEffects` 统一驱动

### 阶段五：部署收尾（1天）

1. 更新 Dockerfile（Nuxt 容器化）
2. 更新 Caddyfile（反代配置）
3. 更新 `docker-compose.yml`
4. 删除废弃文件（`frontend/src/` 旧代码）
5. 端到端测试

---

## 六、不做范围（YAGNI）

- ❌ Rust 插件系统
- ❌ 分布式部署
- ❌ 服务发现 / 插件注册中心
- ❌ PostgreSQL 迁移（SQLite 够用）
- ❌ Redis 缓存
- ❌ WebSocket 实时功能
- ❌ CI/CD 流水线改造（已有 GitHub Actions）
- ❌ 单元测试覆盖（已有基础框架）
- ❌ i18n 国际化
- ❌ 微前端 / 模块联邦
- ❌ AI 功能集成

---

## 七、文件清单

### 新增文件（后端）

| 文件                                        | 说明            |
| ------------------------------------------- | --------------- |
| `backend/src/backend/exceptions.py`         | 统一异常处理器  |
| `backend/src/backend/pagination.py`         | 分页工具类      |
| `backend/src/backend/utils/dependencies.py` | 公共依赖注入    |
| `backend/src/backend/service/storage.py`    | MinIO S3 客户端 |

### 修改文件（后端）

| 文件                   | 修改内容                                     |
| ---------------------- | -------------------------------------------- |
| `database.py`          | 去掉 `get_db()` 自动 commit                  |
| `model/blog.py`        | 统一 `mapped_column()`，去掉 `like` 字段依赖 |
| `model/comment.py`     | 无重大修改                                   |
| `model/user.py`        | 统一 `mapped_column()`                       |
| `router/__init__.py`   | 去掉 `RouterManager`，直接注册               |
| `router/v1/auth.py`    | 合并 register 逻辑                           |
| `router/v1/blog.py`    | 公开 GET 接口，改 `Authorization`            |
| `router/v1/comment.py` | 公开 GET 接口                                |
| `router/v1/user.py`    | 无重大修改                                   |
| `router/v1/admin.py`   | 无重大修改                                   |
| `router/v1/img_bed.py` | 重写为 MinIO S3 存储                         |
| `schema/auth.py`       | 合并 register schema                         |
| `schema/blog.py`       | 去掉 `like` 字段                             |
| `utils/jwt.py`         | 支持 `Authorization: Bearer`                 |
| `config.py`            | 新增 MinIO 配置项                            |

### 新增文件（前端）

| 文件                        | 说明                  |
| --------------------------- | --------------------- |
| `nuxt.config.ts`            | Nuxt 配置             |
| `app.vue`                   | 根组件                |
| `app.config.ts`             | 运行时配置 + 设计令牌 |
| `composables/useAuth.ts`    | 认证 store            |
| `composables/useToast.ts`   | 通知工具              |
| `composables/useEffects.ts` | 统一特效管理器        |
| `utils/api.ts`              | API 请求封装          |
| `middleware/auth.ts`        | 路由守卫              |
| `pages/...`                 | 所有页面文件          |
| `types/...`                 | 类型定义              |

### 删除文件

| 文件                                           | 原因               |
| ---------------------------------------------- | ------------------ |
| `frontend/src/` 整个目录                       | 迁移到 Nuxt 后废弃 |
| `frontend/index.html`                          | Nuxt 自带          |
| `frontend/vite.config.ts`                      | 改用 Nuxt          |
| `backend/src/backend/router/router_manager.py` | 空壳类             |
| `backend/src/backend/router/v1/token.py`       | 合并到 auth        |
| `backend/src/backend/router/v1/register.py`    | 合并到 auth        |
| `backend/src/backend/utils/dependencies.py`    | 空文件             |
| `backend/src/backend/schema/tags.py`           | 空文件             |
| `backend/src/backend/router/v1/background.py`  | 空文件             |
| `frontend/src/stores/userStore.ts`             | 合并到 useAuth     |
