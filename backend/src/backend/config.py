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
    JWT_SECRET_KEY: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

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
