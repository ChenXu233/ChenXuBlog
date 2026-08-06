"""E2E test fixtures: async test client with isolated test database."""
import tempfile
from pathlib import Path
from typing import AsyncGenerator, AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend import app
from backend.config import CONFIG
from backend.database import Base, get_db
from backend.router import router_manager
from backend.utils.first_start import check_is_first_start, first_start


@pytest.fixture(scope="module")
def test_db_path() -> Path:
    """Create a temporary SQLite database for testing."""
    tmpdir = tempfile.mkdtemp()
    return Path(tmpdir) / "test_blog.db"


@pytest_asyncio.fixture(scope="module")
async def test_engine(test_db_path: Path):
    """Create an isolated engine for tests."""
    test_db_uri = f"sqlite+aiosqlite:///{test_db_path}"
    engine = create_async_engine(test_db_uri, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="module")
async def test_session_factory(test_engine):
    """Create a session factory for the test database."""
    return async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="module")
async def test_app(test_engine, test_session_factory):
    """Override get_db dependency and register routers for testing."""
    router_manager.init_router(app)

    # Track whether first_start has been run
    _first_start_done = False

    async def override_get_db():
        nonlocal _first_start_done
        async with test_session_factory() as session:
            if not _first_start_done:
                if await check_is_first_start(session):
                    await first_start(session)
                _first_start_done = True
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="module")
async def client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client for the test app."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="module")
async def admin_token(client: AsyncClient) -> str:
    """Log in as admin and return the access token."""
    response = await client.post(
        "/apis/v1/auth/login",
        json={"evidence": "admin", "password": CONFIG.ADMIN_PASSWORD},
    )
    assert response.status_code == 200, f"Admin login failed: {response.text}"
    return response.json()["access_token"]


@pytest_asyncio.fixture(scope="module")
async def admin_auth_headers(admin_token: str) -> dict:
    """Return Authorization header for admin."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest_asyncio.fixture(scope="module")
async def user_token(client: AsyncClient) -> str:
    """Register a test user, log in, return access token."""
    response = await client.post(
        "/apis/v1/auth/register",
        json={
            "username": "testuser",
            "password": "TestPass123!",
            "email": "testuser@example.com",
        },
    )
    assert response.status_code == 200, f"Register failed: {response.text}"
    response = await client.post(
        "/apis/v1/auth/login",
        json={"evidence": "testuser", "password": "TestPass123!"},
    )
    assert response.status_code == 200, f"User login failed: {response.text}"
    return response.json()["access_token"]


@pytest_asyncio.fixture(scope="module")
async def user_auth_headers(user_token: str) -> dict:
    """Return Authorization header for test user."""
    return {"Authorization": f"Bearer {user_token}"}


@pytest_asyncio.fixture(scope="module")
async def test_blog_id(client: AsyncClient, user_auth_headers: dict) -> int:
    """Create a test blog and return its ID."""
    response = await client.post(
        "/apis/v1/blog/",
        json={
            "title": "Test Blog Post",
            "body": "This is a test blog post body.",
            "tags": ["test", "e2e"],
            "published": True,
        },
        headers=user_auth_headers,
    )
    assert response.status_code == 200, f"Create blog failed: {response.text}"
    return response.json()["id"]


@pytest_asyncio.fixture(scope="module")
async def test_comment_id(
    client: AsyncClient, user_auth_headers: dict, test_blog_id: int
) -> int:
    """Create a test comment and return its ID."""
    response = await client.post(
        "/apis/v1/comment/create",
        json={"blog_id": test_blog_id, "content": "Test comment content"},
        headers=user_auth_headers,
    )
    assert response.status_code == 200, f"Create comment failed: {response.text}"
    return response.json()["id"]