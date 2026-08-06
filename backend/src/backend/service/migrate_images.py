"""Migrate existing local images to MinIO storage.

Usage: cd backend && python -m backend.service.migrate_images
"""

import asyncio
from pathlib import Path

from backend.config import CONFIG
from backend.service.storage import storage_service
from backend.logger import logger


async def migrate_images():
    """Migrate all images from local filesystem to MinIO."""
    image_dir = CONFIG.IMAGE_BED_PATH
    if not image_dir.exists():
        logger.info(f"No image directory found at {image_dir}")
        return

    files = list(image_dir.iterdir())
    if not files:
        logger.info("No images to migrate")
        return

    logger.info(f"Found {len(files)} files to migrate from {image_dir}")
    migrated = 0
    skipped = 0
    failed = 0

    for file_path in files:
        if not file_path.is_file():
            continue

        try:
            data = file_path.read_bytes()
            # Guess content type
            ext = file_path.suffix.lower()
            content_type = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".svg": "image/svg+xml",
                ".bmp": "image/bmp",
            }.get(ext, "application/octet-stream")

            url = await storage_service.upload(data, content_type)
            logger.info(f"  ✓ {file_path.name} → {url}")
            migrated += 1
        except Exception as e:
            logger.error(f"  ✗ {file_path.name}: {e}")
            failed += 1

    logger.info(f"Migration complete: {migrated} migrated, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    asyncio.run(migrate_images())