from pathlib import Path

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    # 定义配置项
    APP_NAME: str = "ChenXuBlog"
    LOG_LEVEL: str = "DEBUG"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite+aiosqlite:///./database/blog.db"
    LOG_PATH: Path = Path("./logs")
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"  # 指定 .env 文件路径
        env_file_encoding = "utf-8"  # 指定文件编码

    @classmethod
    def validate_log_path(cls, value: str) -> Path:
        return Path(value)


CONFIG = AppConfig()  # type: ignore
print(CONFIG.model_dump())  # 打印配置项

# 示例：打印配置
if __name__ == "__main__":
    print(CONFIG.model_dump())
