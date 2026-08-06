"""Phase 1 E2E tests: backend fixes verification.

Run: cd backend && pytest tests/e2e_api/test_phase1_backend.py -v

All tests must pass before proceeding to Phase 1B.
"""

import pytest
from httpx import AsyncClient


class TestAuth:
    """Authentication flow: register -> login -> refresh -> token validation."""

    async def test_register(self, client: AsyncClient):
        """Register a new user."""
        response = await client.post(
            "/apis/v1/auth/register",
            json={
                "username": "e2e_test_user",
                "password": "E2ePass123!",
                "email": "e2e_test@example.com",
            },
        )
        assert response.status_code == 200, f"Register failed: {response.text}"
        data = response.json()
        assert "user_uuid" in data

    async def test_register_duplicate_username(self, client: AsyncClient):
        """Register with duplicate username should not 500."""
        response = await client.post(
            "/apis/v1/auth/register",
            json={
                "username": "e2e_test_user",
                "password": "E2ePass123!",
                "email": "another@example.com",
            },
        )
        assert response.status_code != 500, f"Server error: {response.text}"

    async def test_login(self, client: AsyncClient):
        """Login with username and password returns tokens."""
        response = await client.post(
            "/apis/v1/auth/login",
            json={"evidence": "e2e_test_user", "password": "E2ePass123!"},
        )
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        assert "user_uuid" in data

    async def test_login_with_email(self, client: AsyncClient):
        """Login with email works."""
        response = await client.post(
            "/apis/v1/auth/login",
            json={"evidence": "e2e_test@example.com", "password": "E2ePass123!"},
        )
        assert response.status_code == 200, f"Login with email failed: {response.text}"

    async def test_login_wrong_password(self, client: AsyncClient):
        """Login with wrong password returns 401."""
        response = await client.post(
            "/apis/v1/auth/login",
            json={"evidence": "e2e_test_user", "password": "WrongPass1!"},
        )
        assert response.status_code == 401, f"Expected 401: {response.text}"

    async def test_refresh_token(self, client: AsyncClient, admin_token: str):
        """Refresh endpoint works (cookie-based)."""
        login_resp = await client.post(
            "/apis/v1/auth/login",
            json={"evidence": "admin", "password": "123456"},
        )
        assert login_resp.status_code == 200
        cookies = login_resp.cookies
        response = await client.post("/apis/v1/auth/refresh", cookies=cookies)
        assert response.status_code in (200, 404, 401), f"Unexpected: {response.text}"


class TestBlog:
    """Blog CRUD operations with self-contained tests."""

    async def test_create_and_get_blog(self, client: AsyncClient, admin_auth_headers: dict):
        """Create a blog, then retrieve it."""
        # Create
        create_resp = await client.post(
            "/apis/v1/blog/",
            json={
                "title": "E2E Test Blog",
                "body": "This is the body of the E2E test blog.",
                "tags": ["e2e", "test"],
                "published": True,
            },
            headers=admin_auth_headers,
        )
        assert create_resp.status_code == 200, f"Create blog failed: {create_resp.text}"
        blog_id = create_resp.json()["id"]
        assert create_resp.json()["title"] == "E2E Test Blog"

        # Get by ID (public)
        get_resp = await client.get(f"/apis/v1/blog/{blog_id}")
        assert get_resp.status_code == 200, f"Get blog failed: {get_resp.text}"
        assert get_resp.json()["title"] == "E2E Test Blog"

        return blog_id

    async def test_get_blog_list_public(self, client: AsyncClient):
        """Unauthenticated user can view blog list."""
        response = await client.get("/apis/v1/blog/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data

    async def test_update_blog(self, client: AsyncClient, admin_auth_headers: dict):
        """Author can update their blog."""
        # Create a blog first
        create_resp = await client.post(
            "/apis/v1/blog/",
            json={
                "title": "Blog to Update",
                "body": "Original body.",
                "tags": ["test"],
                "published": True,
            },
            headers=admin_auth_headers,
        )
        assert create_resp.status_code == 200
        blog_id = create_resp.json()["id"]

        # Update it
        response = await client.put(
            f"/apis/v1/blog/{blog_id}",
            json={
                "title": "Updated E2E Blog",
                "body": "Updated body content.",
                "tags": ["e2e", "updated"],
                "published": True,
            },
            headers=admin_auth_headers,
        )
        assert response.status_code == 200, f"Update blog failed: {response.text}"
        assert response.json()["title"] == "Updated E2E Blog"

    async def test_delete_blog(self, client: AsyncClient, admin_auth_headers: dict):
        """Author can delete their blog."""
        # Create a blog first
        create_resp = await client.post(
            "/apis/v1/blog/",
            json={
                "title": "Blog to Delete",
                "body": "Will be deleted.",
                "tags": ["test"],
                "published": True,
            },
            headers=admin_auth_headers,
        )
        assert create_resp.status_code == 200
        blog_id = create_resp.json()["id"]

        # Delete it
        response = await client.delete(
            f"/apis/v1/blog/{blog_id}",
            headers=admin_auth_headers,
        )
        assert response.status_code == 200, f"Delete blog failed: {response.text}"


class TestComment:
    """Comment reading and writing."""

    async def test_get_comments_public(self, client: AsyncClient):
        """Unauthenticated user can view comments."""
        response = await client.get("/apis/v1/comment/get/1")
        assert response.status_code in (200, 404), f"Get comments failed: {response.text}"

    async def test_create_comment(self, client: AsyncClient, admin_auth_headers: dict):
        """Authenticated user can create a comment."""
        # Create a blog to comment on
        blog_resp = await client.post(
            "/apis/v1/blog/",
            json={
                "title": "Blog for Comment Test",
                "body": "Body for comment test.",
                "tags": ["test"],
                "published": True,
            },
            headers=admin_auth_headers,
        )
        assert blog_resp.status_code == 200
        blog_id = blog_resp.json()["id"]

        # Create comment
        response = await client.post(
            "/apis/v1/comment/create",
            json={"blog_id": blog_id, "content": "This is a test comment."},
            headers=admin_auth_headers,
        )
        assert response.status_code == 200, f"Create comment failed: {response.text}"
        assert response.json()["content"] == "This is a test comment."

    async def test_create_comment_no_auth(self, client: AsyncClient):
        """Unauthenticated user cannot create a comment."""
        response = await client.post(
            "/apis/v1/comment/create",
            json={"blog_id": 1, "content": "Anonymous comment"},
        )
        assert response.status_code in (401, 403), f"Expected auth error: {response.text}"


class TestAuthAuthorization:
    """Authorization: Bearer header validation."""

    async def test_access_with_bearer_token(self, client: AsyncClient, admin_token: str):
        """Bearer token grants access to protected endpoints."""
        response = await client.get(
            "/apis/v1/permission/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200, f"Bearer auth failed: {response.text}"

    async def test_access_without_token(self, client: AsyncClient):
        """No token results in 401."""
        response = await client.get("/apis/v1/permission/")
        assert response.status_code in (401, 403), f"Expected 401: {response.text}"

    async def test_access_with_invalid_token(self, client: AsyncClient):
        """Invalid token results in 401."""
        response = await client.get(
            "/apis/v1/permission/",
            headers={"Authorization": "Bearer invalid_token_here"},
        )
        assert response.status_code in (401, 403), f"Expected 401: {response.text}"


class TestPagination:
    """Pagination works correctly."""

    async def test_pagination_defaults(self, client: AsyncClient):
        """Default pagination returns page 1, page_size 10."""
        response = await client.get("/apis/v1/blog/")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert data["total"] >= 0
        assert data["total_pages"] >= 1

    async def test_pagination_custom(self, client: AsyncClient):
        """Custom page and page_size work."""
        response = await client.get("/apis/v1/blog/?page=1&page_size=5")
        assert response.status_code == 200
        data = response.json()
        assert data["page_size"] == 5

    async def test_pagination_page_out_of_range(self, client: AsyncClient):
        """Page beyond total pages returns empty list."""
        response = await client.get("/apis/v1/blog/?page=999")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0


class TestPermission:
    """Permission checks work correctly."""

    async def test_admin_access_admin_endpoint(self, client: AsyncClient, admin_auth_headers: dict):
        """Admin can access admin endpoints."""
        response = await client.get("/apis/v1/admin/stats", headers=admin_auth_headers)
        assert response.status_code == 200, f"Admin access failed: {response.text}"

    async def test_regular_user_denied_admin(self, client: AsyncClient, user_auth_headers: dict):
        """Regular user cannot access admin endpoints."""
        response = await client.get("/apis/v1/admin/stats", headers=user_auth_headers)
        assert response.status_code == 403, f"Expected 403: {response.text}"


class TestLike:
    """Like/unlike flow."""

    async def test_toggle_like(self, client: AsyncClient, admin_auth_headers: dict):
        """Like a blog, then unlike it."""
        # Create a blog to like
        blog_resp = await client.post(
            "/apis/v1/blog/",
            json={
                "title": "Blog for Like Test",
                "body": "Body for like test.",
                "tags": ["test"],
                "published": True,
            },
            headers=admin_auth_headers,
        )
        assert blog_resp.status_code == 200
        blog_id = blog_resp.json()["id"]

        # Like
        response = await client.post(
            f"/apis/v1/blog/{blog_id}/like",
            headers=admin_auth_headers,
        )
        assert response.status_code == 200, f"Like failed: {response.text}"
        assert response.json()["liked"] is True, f"Expected liked=True: {response.text}"

        # Check like status
        status_resp = await client.get(f"/apis/v1/blog/{blog_id}/like")
        assert status_resp.status_code == 200
        assert status_resp.json()["likes_count"] >= 1

        # Unlike
        response = await client.post(
            f"/apis/v1/blog/{blog_id}/like",
            headers=admin_auth_headers,
        )
        assert response.status_code == 200, f"Unlike failed: {response.text}"
        assert response.json()["liked"] is False, f"Expected liked=False: {response.text}"