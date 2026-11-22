"""MinIO S3-compatible storage router.

Supports both MinIO (when configured) and local filesystem fallback.
"""

import io
import warnings

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError

from backend.schema.img_bed import ImageUploadResponse
from backend.service.storage import storage_service
from backend.utils.permission import require_permissions

img_bed = APIRouter(prefix="/apis/v1/img_bed", tags=["img_bed"])

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 40_000_000
ALLOWED_IMAGE_FORMATS = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "GIF": "image/gif",
    "WEBP": "image/webp",
}
ALLOWED_DECLARED_TYPES = {
    *ALLOWED_IMAGE_FORMATS.values(),
    "image/jpg",
    "application/octet-stream",
}


def validate_image_bytes(data: bytes, declared_content_type: str | None = None) -> str:
    """Validate the actual image and return a trusted MIME type."""
    if declared_content_type and declared_content_type not in ALLOWED_DECLARED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported image content type")

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as image:
                image_format = image.format or ""
                width, height = image.size
                if width * height > MAX_IMAGE_PIXELS:
                    raise HTTPException(
                        status_code=413,
                        detail=f"Image exceeds the {MAX_IMAGE_PIXELS:,} pixel limit",
                    )
                image.verify()
    except HTTPException:
        raise
    except (
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
        UnidentifiedImageError,
        OSError,
        SyntaxError,
    ) as exc:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image") from exc

    if image_format not in ALLOWED_IMAGE_FORMATS:
        raise HTTPException(status_code=415, detail="Only JPEG, PNG, GIF and WebP images are allowed")
    return ALLOWED_IMAGE_FORMATS[image_format]


async def read_image_upload(
    image: UploadFile, max_bytes: int = MAX_IMAGE_BYTES
) -> tuple[bytes, str]:
    """Read at most max_bytes + 1 bytes and validate the upload."""
    try:
        data = await image.read(max_bytes + 1)
        if not data:
            raise HTTPException(status_code=400, detail="Empty file")
        if len(data) > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"Image exceeds the {max_bytes // (1024 * 1024)} MiB limit",
            )
        content_type = validate_image_bytes(data, image.content_type)
        return data, content_type
    finally:
        await image.close()


@img_bed.post(
    "/",
    name="image_upload",
    response_model=ImageUploadResponse,
    dependencies=[Depends(require_permissions("img_bed:create", "Upload image"))],
)
async def upload_image(image: UploadFile = File(...)):
    """Upload a verified image file and return its public URL."""
    data, content_type = await read_image_upload(image)
    url = await storage_service.upload(data, content_type)
    return {"url": url}


@img_bed.get(
    "/{object_name}",
    name="image_get",
)
async def get_image(object_name: str):
    """Get an image file by its hash-based filename."""
    data = await storage_service.get(object_name)
    if data is None:
        raise HTTPException(status_code=404, detail="Image not found")

    ext = object_name.rsplit(".", 1)[-1].lower() if "." in object_name else ""
    content_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "svg": "image/svg+xml",
        "bmp": "image/bmp",
    }.get(ext, "application/octet-stream")

    return Response(
        content=data,
        media_type=content_type,
        headers={"X-Content-Type-Options": "nosniff"},
    )
