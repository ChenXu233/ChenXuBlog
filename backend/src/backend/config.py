from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    # 定义配置项
    APP_NAME: str = "ChenXuBlog"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"
    DEBUG: bool = False
    DATABASE_URI: str = "sqlite+aiosqlite:///./data/database/blog.db"
    IMG_PATH: Path = Path("./data/images")
    LOG_PATH: Path = Path("./logs")
    IMAGE_BED_PATH: Path = Path("./data/images")
    PORT: int = 8000
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 465
    MAIL_SERVER: str = ""
    MAIL_ENABLED: bool = False  # 设为 false 则只打印邮件内容，不实际发送
    # 前端站点地址，用于邮件/通知里的链接
    SITE_URL: str = "http://localhost:3000"
    # MinIO 配置
    MINIO_ENABLED: bool = False
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "chenxu-blog-images"
    MINIO_SECURE: bool = False
    # 管理员配置
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "123456"
    ADMIN_EMAIL: str = "admin@example.com"

    class Config:
        env_file = ".env"  # 指定 .env 文件路径
        env_file_encoding = "utf-8"  # 指定文件编码
        extra = "allow"

    @model_validator(mode="after")
    def validate_production_security(self):
        """Reject development defaults when running in production."""
        if self.ENVIRONMENT.lower() not in {"prod", "production"}:
            return self

        errors: list[str] = []
        weak_values = {"", "123456", "admin", "password", "minioadmin", "changeme"}

        if self.ADMIN_PASSWORD.lower() in weak_values or len(self.ADMIN_PASSWORD) < 12:
            errors.append("ADMIN_PASSWORD must be a non-default value of at least 12 characters")

        for name in ("ACCESS_SECRET_KEY", "REFRESH_SECRET_KEY"):
            value = getattr(self, name)
            if value.lower() in weak_values or len(value) < 32:
                errors.append(f"{name} must contain at least 32 characters")
        if self.ACCESS_SECRET_KEY == self.REFRESH_SECRET_KEY:
            errors.append("ACCESS_SECRET_KEY and REFRESH_SECRET_KEY must be different")

        if self.MINIO_ENABLED:
            if self.MINIO_ACCESS_KEY.lower() in weak_values:
                errors.append("MINIO_ACCESS_KEY must not use its development default")
            if (
                self.MINIO_SECRET_KEY.lower() in weak_values
                or len(self.MINIO_SECRET_KEY) < 12
            ):
                errors.append("MINIO_SECRET_KEY must be a non-default value of at least 12 characters")

        if errors:
            raise ValueError("Production security configuration invalid: " + "; ".join(errors))
        return self

    @classmethod
    def validate_log_path(cls, value: str) -> Path:
        path = Path(value)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        if not path.is_dir():
            raise ValueError(f"The path {path} is not a directory.")
        return path


CONFIG = AppConfig()  # type: ignore

# 示例：打印配置
if __name__ == "__main__":
    print(CONFIG.model_dump())
