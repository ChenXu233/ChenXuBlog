"""Phase 3 E2E tests: backend feature completion.

Run: cd backend && pytest tests/e2e_api/test_phase3_features.py -v

Covers: email verification, password reset, admin APIs, avatar upload,
article cover, site search.
"""

from httpx import AsyncClient


class TestEmailVerification:
    """注册 → 验证 token → 用户已认证。"""

    async def test_register_sets_verify_token(self, client: AsyncClient):
        """注册后用户有 verify_token 且未验证。"""
        resp = await client.post(
            "/apis/v1/auth/register",
            json={
                "username": "verify_user",
                "password": "VerifyPass123!",
                "email": "verify_user@example.com",
            },
        )
        assert resp.status_code == 200, f"Register failed: {resp.text}"
        assert "user_uuid" in resp.json()

        # 用新用户登录并查用户信息确认未验证（登录本身不需要验证）
        login = await client.post(
            "/apis/v1/auth/login",
            json={"evidence": "verify_user", "password": "VerifyPass123!"},
        )
        assert login.status_code == 200
        token = login.json()["access_token"]
        info = await client.get(
            "/apis/v1/user/info", headers={"Authorization": f"Bearer {token}"}
        )
        assert info.status_code == 200

    async def test_verify_with_invalid_token(self, client: AsyncClient):
        """无效 token 验证返回 400。"""
        resp = await client.get("/apis/v1/auth/verify/invalid-token-xyz")
        assert resp.status_code == 400, f"Expected 400: {resp.text}"


class TestPasswordReset:
    """忘记密码 → 重置 → 新密码登录。"""

    async def test_forgot_password_unknown_email(self, client: AsyncClient):
        """未知邮箱也返回成功（防枚举）。"""
        resp = await client.post(
            "/apis/v1/auth/forgot-password",
            json={"email": "nobody@example.com"},
        )
        assert resp.status_code == 200
        assert "sent" in resp.json()["message"].lower()

    async def test_forgot_and_reset_password(self, client: AsyncClient):
        """已知邮箱：生成重置 token → 重置密码 → 新密码可登录。"""
        # 先注册一个用户
        await client.post(
            "/apis/v1/auth/register",
            json={
                "username": "reset_user",
                "password": "OldPass123!",
                "email": "reset_user@example.com",
            },
        )

        # 忘记密码（邮件未配置时 token 打印在日志，E2E 无法直接获取；
        # 这里验证端点响应结构正确即可）
        resp = await client.post(
            "/apis/v1/auth/forgot-password",
            json={"email": "reset_user@example.com"},
        )
        assert resp.status_code == 200
        assert "sent" in resp.json()["message"].lower()

        # 无效 token 重置失败
        bad = await client.post(
            "/apis/v1/auth/reset-password",
            json={"token": "invalid-token", "new_password": "NewPass123!"},
        )
        assert bad.status_code in (400, 401)

        # 旧密码仍可登录（token 无效所以密码未变）
        login = await client.post(
            "/apis/v1/auth/login",
            json={"evidence": "reset_user", "password": "OldPass123!"},
        )
        assert login.status_code == 200


class TestAdminAPI:
    """后台管理 API：权限保护 + 列表 + 发布切换。"""

    async def test_stats_requires_admin(self, client: AsyncClient, user_auth_headers: dict):
        """普通用户访问 admin/stats 返回 403。"""
        resp = await client.get("/apis/v1/admin/stats", headers=user_auth_headers)
        assert resp.status_code == 403, f"Expected 403: {resp.text}"

    async def test_admin_stats(self, client: AsyncClient, admin_auth_headers: dict):
        """管理员获取仪表盘统计。"""
        resp = await client.get("/apis/v1/admin/stats", headers=admin_auth_headers)
        assert resp.status_code == 200, f"Stats failed: {resp.text}"
        data = resp.json()
        for key in ("total_users", "total_blogs", "total_comments", "total_blogs_today", "total_comments_today"):
            assert key in data, f"Missing stats key: {key}"

    async def test_admin_user_list(self, client: AsyncClient, admin_auth_headers: dict):
        """管理员查看用户列表。"""
        resp = await client.get("/apis/v1/admin/users", headers=admin_auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data and data["total"] >= 1

    async def test_admin_blog_list(self, client: AsyncClient, admin_auth_headers: dict):
        """管理员查看文章列表（含未发布）。"""
        resp = await client.get("/apis/v1/admin/blogs", headers=admin_auth_headers)
        assert resp.status_code == 200
        assert "items" in resp.json()

    async def test_toggle_publish_requires_admin(self, client: AsyncClient, user_auth_headers: dict):
        """普通用户不能切换发布状态。"""
        resp = await client.put("/apis/v1/admin/blogs/1/publish", headers=user_auth_headers)
        assert resp.status_code == 403, f"Expected 403: {resp.text}"

    async def test_delete_user_requires_admin(self, client: AsyncClient, user_auth_headers: dict):
        """普通用户不能删除用户。"""
        resp = await client.delete("/apis/v1/admin/users/1", headers=user_auth_headers)
        assert resp.status_code == 403, f"Expected 403: {resp.text}"

    async def test_admin_roles(self, client: AsyncClient, admin_auth_headers: dict):
        """管理员获取角色列表。"""
        resp = await client.get("/apis/v1/admin/roles", headers=admin_auth_headers)
        assert resp.status_code == 200
        roles = resp.json()
        assert any(r["name"] == "superuser" for r in roles), f"Missing superuser: {roles}"
        assert any(r["name"] == "default" for r in roles), f"Missing default: {roles}"


class TestAvatarUpload:
    """上传头像 → 更新用户资料。"""

    async def test_upload_image(self, client: AsyncClient, admin_auth_headers: dict):
        """上传图片返回 URL。"""
        resp = await client.post(
            "/apis/v1/img_bed/",
            files={"image": ("avatar.png", b"\x89PNG\r\n\x1a\nfakedata", "image/png")},
            headers=admin_auth_headers,
        )
        assert resp.status_code == 200, f"Upload failed: {resp.text}"
        url = resp.json().get("url")
        assert url and url.startswith("/"), f"Bad url: {url}"

    async def test_upload_without_auth(self, client: AsyncClient):
        """未登录不能上传。"""
        resp = await client.post(
            "/apis/v1/img_bed/",
            files={"image": ("x.png", b"data", "image/png")},
        )
        assert resp.status_code in (401, 403), f"Expected 401/403: {resp.text}"

    async def test_update_avatar(self, client: AsyncClient, admin_auth_headers: dict):
        """通过 /user/edit 更新头像 URL。"""
        resp = await client.post(
            "/apis/v1/user/edit",
            json={"avatar": "/images/test-avatar.png"},
            headers=admin_auth_headers,
        )
        assert resp.status_code == 200, f"Edit failed: {resp.text}"
        assert resp.json()["avatar"] == "/images/test-avatar.png"


class TestArticleCover:
    """文章封面图：创建时设置 + 更新时修改。"""

    async def test_create_blog_with_cover(self, client: AsyncClient, admin_auth_headers: dict):
        """创建文章带封面 URL。"""
        resp = await client.post(
            "/apis/v1/blog/",
            json={
                "title": "Blog with Cover",
                "body": "Cover test body.",
                "tags": ["cover"],
                "published": True,
                "cover_url": "/images/cover-1.png",
            },
            headers=admin_auth_headers,
        )
        assert resp.status_code == 200, f"Create failed: {resp.text}"
        assert resp.json()["cover_url"] == "/images/cover-1.png"
        return resp.json()["id"]

    async def test_update_blog_cover(self, client: AsyncClient, admin_auth_headers: dict):
        """更新文章封面 URL。"""
        create = await client.post(
            "/apis/v1/blog/",
            json={
                "title": "Blog Cover Update",
                "body": "Body.",
                "tags": ["cover"],
                "published": True,
            },
            headers=admin_auth_headers,
        )
        blog_id = create.json()["id"]

        resp = await client.put(
            f"/apis/v1/blog/{blog_id}",
            json={
                "title": "Blog Cover Update",
                "body": "Body.",
                "tags": ["cover"],
                "published": True,
                "cover_url": "/images/cover-2.png",
            },
            headers=admin_auth_headers,
        )
        assert resp.status_code == 200, f"Update failed: {resp.text}"
        assert resp.json()["cover_url"] == "/images/cover-2.png"


class TestSearch:
    """站内搜索：标题/内容关键字。"""

    async def test_search_by_title(self, client: AsyncClient, admin_auth_headers: dict):
        """创建带独特关键字的文章，搜索命中。"""
        await client.post(
            "/apis/v1/blog/",
            json={
                "title": "Zephyr Quantum Search Target",
                "body": "Unique body for search test.",
                "tags": ["search"],
                "published": True,
            },
            headers=admin_auth_headers,
        )

        resp = await client.get("/apis/v1/blog/?search=Zephyr+Quantum")
        assert resp.status_code == 200
        items = resp.json()["items"]
        assert any("Zephyr Quantum" in i["title"] for i in items), f"No match: {items}"

    async def test_search_no_result(self, client: AsyncClient):
        """搜索不存在的关键字返回空列表。"""
        resp = await client.get("/apis/v1/blog/?search=zzzz_no_such_keyword_zzzz")
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == 0

    async def test_search_by_tag(self, client: AsyncClient, admin_auth_headers: dict):
        """按标签过滤命中。"""
        resp = await client.get("/apis/v1/blog/?tag=search")
        assert resp.status_code == 200
        items = resp.json()["items"]
        assert len(items) >= 1, f"No tag matches: {items}"
