from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    # 定义配置项
    app_name: str = "ChenXuBlog"
    debug: bool = False
    database_url: str = "sqlite:///./database/blog.db"
    log_path: str = "./logs"
    key: str

    class Config:
        env_file = ".env"  # 指定 .env 文件路径
        env_file_encoding = "utf-8"  # 指定文件编码


CONFIG = AppConfig()  # type: ignore

# 示例：打印配置
if __name__ == "__main__":
    print(CONFIG.model_dump())
