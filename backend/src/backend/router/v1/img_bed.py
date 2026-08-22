"""MinIO S3 image storage router.

Supports both MinIO (when configured) and local filesystem fallback.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response

from backend.schema.img_bed import ImageUploadResponse
from backend.service.storage import storage_service
from backend.utils.permission import require_permissions

img_bed = APIRouter(prefix="/apis/v1/img_bed", tags=["img_bed"])


@img_bed.post(
    "/",
    name="image_upload",
    response_model=ImageUploadResponse,
    dependencies=[Depends(require_permissions("img_bed:create", "Upload image"))],
)
async def upload_image(image: UploadFile = File(...)):
    """Upload an image file. Returns the public URL.

    The file is stored via StorageService (MinIO or local filesystem).
    """
    data = await image.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    url = await storage_service.upload(data, image.content_type or "application/octet-stream")
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

    # Guess content type from extension
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

    return Response(content=data, media_type=content_type)