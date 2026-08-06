"""MinIO S3-compatible storage service for image uploads."""

import hashlib
import io
import os
from pathlib import Path
from typing import Optional

from minio import Minio
from minio.error import S3Error

from backend.config import CONFIG
from backend.logger import logger


class StorageService:
    """MinIO S3 存储服务，管理图片上传/读取。"""

    def __init__(self):
        self.client: Optional[Minio] = None
        self.bucket = CONFIG.MINIO_BUCKET
        self._local_dir = CONFIG.IMAGE_BED_PATH
        self._use_minio = CONFIG.MINIO_ENABLED

        if self._use_minio:
            self._init_minio()
        else:
            logger.info(f"MinIO disabled, using local filesystem: {self._local_dir}")
            self._local_dir.mkdir(parents=True, exist_ok=True)

    def _init_minio(self):
        """Initialize MinIO client and ensure bucket exists."""
        try:
            self.client = Minio(
                CONFIG.MINIO_ENDPOINT,
                access_key=CONFIG.MINIO_ACCESS_KEY,
                secret_key=CONFIG.MINIO_SECRET_KEY,
                secure=CONFIG.MINIO_SECURE,
            )
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
                logger.info(f"Created MinIO bucket: {self.bucket}")
            logger.info(f"MinIO connected: {CONFIG.MINIO_ENDPOINT}/{self.bucket}")
        except Exception as e:
            logger.warning(f"MinIO init failed, falling back to local storage: {e}")
            self.client = None
            self._use_minio = False
            self._local_dir.mkdir(parents=True, exist_ok=True)

    async def upload(self, file_data: bytes, content_type: str = "application/octet-stream") -> str:
        """Upload a file, return its URL path."""
        file_hash = hashlib.sha256(file_data).hexdigest()
        ext = self._guess_extension(content_type)
        object_name = f"{file_hash}{ext}"

        if self._use_minio and self.client:
            try:
                self.client.put_object(
                    self.bucket, object_name,
                    io.BytesIO(file_data), len(file_data),
                    content_type=content_type,
                )
                logger.info(f"Uploaded to MinIO: {object_name}")
            except S3Error as e:
                logger.error(f"MinIO upload failed: {e}")
                raise
        else:
            # Local fallback
            file_path = self._local_dir / object_name
            if not file_path.exists():
                file_path.write_bytes(file_data)
                logger.info(f"Saved locally: {file_path}")

        return f"/images/{object_name}"

    async def get(self, object_name: str) -> Optional[bytes]:
        """Get file content by object name."""
        if self._use_minio and self.client:
            try:
                response = self.client.get_object(self.bucket, object_name)
                data = response.read()
                response.close()
                response.release_conn()
                return data
            except S3Error as e:
                logger.warning(f"MinIO get failed: {e}")
                return None
        else:
            file_path = self._local_dir / object_name
            if file_path.exists():
                return file_path.read_bytes()
            return None

    async def delete(self, object_name: str) -> bool:
        """Delete a file by object name."""
        if self._use_minio and self.client:
            try:
                self.client.remove_object(self.bucket, object_name)
                return True
            except S3Error:
                return False
        else:
            file_path = self._local_dir / object_name
            if file_path.exists():
                file_path.unlink()
                return True
            return False

    def _guess_extension(self, content_type: str) -> str:
        """Guess file extension from content type."""
        mapping = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/svg+xml": ".svg",
            "image/bmp": ".bmp",
        }
        return mapping.get(content_type, ".bin")


# 全局单例
storage_service = StorageService()