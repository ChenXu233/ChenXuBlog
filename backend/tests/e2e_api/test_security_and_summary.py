import io
from math import ceil

import pytest
from fastapi import HTTPException, UploadFile
from httpx import AsyncClient
from PIL import Image
from pydantic import ValidationError
from sqlalchemy import select
from starlette.datastructures import Headers

from backend.config import AppConfig
from backend.model.blog import Blog
from backend.model.user import User
from backend.router.v1.img_bed import read_image_upload, validate_image_bytes
from backend.utils.excerpt import make_excerpt


def make_image_bytes(image_format: str = "PNG") -> bytes:
    output = io.BytesIO()
    Image.new("RGB", (2, 2), color=(227, 68, 28)).save(output, format=image_format)
    return output.getvalue()


def make_production_config(**overrides) -> AppConfig:
    values = {
        "_env_file": None,
        "ENVIRONMENT": "production",
        "ACCESS_SECRET_KEY": "a" * 32,
        "REFRESH_SECRET_KEY": "b" * 32,
        "ADMIN_PASSWORD": "a-secure-admin-password",
        "MINIO_ENABLED": False,
    }
    values.update(overrides)
    return AppConfig(**values)


class TestProductionConfig:
    def test_valid_production_config(self):
        config = make_production_config(
            MINIO_ENABLED=True,
            MINIO_ACCESS_KEY="blog-production",
            MINIO_SECRET_KEY="a-secure-minio-secret",
        )
        assert config.ENVIRONMENT == "production"

    @pytest.mark.parametrize(
        "overrides",
        [
            {"ADMIN_PASSWORD": "123456"},
            {"ACCESS_SECRET_KEY": "too-short"},
            {"REFRESH_SECRET_KEY": "a" * 32},
            {"MINIO_ENABLED": True},
        ],
    )
    def test_rejects_weak_production_config(self, overrides):
        with pytest.raises(ValidationError, match="Production security configuration invalid"):
            make_production_config(**overrides)


class TestImageValidation:
    def test_real_format_determines_content_type(self):
        assert validate_image_bytes(make_image_bytes(), "image/jpeg") == "image/png"

    @pytest.mark.parametrize(
        ("data", "declared_type", "status_code"),
        [
            (b"not an image", "image/png", 400),
            (b"<svg xmlns='http://www.w3.org/2000/svg'/>", "image/svg+xml", 415),
            (make_image_bytes("BMP"), "image/bmp", 415),
        ],
    )
    def test_rejects_invalid_or_unsupported_images(
        self, data: bytes, declared_type: str, status_code: int
    ):
        with pytest.raises(HTTPException) as error:
            validate_image_bytes(data, declared_type)
        assert error.value.status_code == status_code

    async def test_rejects_oversized_upload_before_parsing(self):
        upload = UploadFile(
            file=io.BytesIO(b"x" * 32),
            filename="large.png",
            headers=Headers({"content-type": "image/png"}),
        )
        with pytest.raises(HTTPException) as error:
            await read_image_upload(upload, max_bytes=8)
        assert error.value.status_code == 413


class TestBlogSummary:
    def test_excerpt_removes_markdown_and_limits_length(self):
        excerpt = make_excerpt(
            """# Heading

[read more](https://example.com)

```py
secret()
```

"""
            + "body " * 100,
            max_length=80,
        )
        assert "Heading" in excerpt
        assert "read more" in excerpt
        assert "secret" not in excerpt
        assert "https://" not in excerpt
        assert len(excerpt) <= 81

    async def test_list_has_summary_and_detail_keeps_body(
        self,
        client: AsyncClient,
        admin_auth_headers: dict,
        user_auth_headers: dict,
    ):
        body = """# Summary title

[Summary link](https://example.com)

Full body remains available."""
        created = await client.post(
            "/apis/v1/blog/",
            json={
                "title": "Unique Summary Contract Article",
                "body": body,
                "tags": ["summary"],
                "published": True,
            },
            headers=admin_auth_headers,
        )
        assert created.status_code == 200, created.text
        blog_id = created.json()["id"]

        for headers in (admin_auth_headers, user_auth_headers):
            liked = await client.post(f"/apis/v1/blog/{blog_id}/like", headers=headers)
            assert liked.status_code == 200, liked.text

        response = await client.get("/apis/v1/blog/?search=Unique+Summary+Contract")
        assert response.status_code == 200, response.text
        item = response.json()["items"][0]
        assert "body" not in item
        assert "Summary link" in item["excerpt"]
        assert item["likes_count"] == 2

        detail = await client.get(f"/apis/v1/blog/{blog_id}")
        assert detail.status_code == 200
        assert detail.json()["body"] == body

    async def test_public_list_paginates_beyond_one_hundred(
        self,
        client: AsyncClient,
        test_session_factory,
        admin_auth_headers: dict,
    ):
        async with test_session_factory() as session:
            admin = await session.scalar(select(User).where(User.username == "admin"))
            session.add_all(
                [
                    Blog(
                        user_uuid=admin.uuid,
                        title=f"Bulk pagination {index}",
                        body="Pagination body",
                        published=True,
                    )
                    for index in range(101)
                ]
            )
            await session.commit()

        first = await client.get("/apis/v1/blog/?page=1&page_size=100")
        second = await client.get("/apis/v1/blog/?page=2&page_size=100")
        assert first.status_code == 200, first.text
        assert second.status_code == 200, second.text
        first_data = first.json()
        assert len(first_data["items"]) == 100
        assert len(second.json()["items"]) >= 1
        assert first_data["total_pages"] == ceil(first_data["total"] / 100)
        assert all("body" not in item for item in first_data["items"])
