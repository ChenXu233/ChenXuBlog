from pathlib import Path

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    # 定义配置项
    APP_NAME: str = "ChenXuBlog"
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

    @classmethod
    def validate_log_path(cls, value: str) -> Path:
        path = Path(value)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        if not path.is_dir():
            raise ValueError(f"The path {path} is not a directory.")
        return path


CONFIG = AppConfig()  # type: ignore
print(CONFIG.model_dump())  # 打印配置项

# 示例：打印配置
if __name__ == "__main__":
    print(CONFIG.model_dump())
