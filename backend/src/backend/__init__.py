from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from backend.logger import logger

from .config import CONFIG
from .database import get_db, init_db
from .router import router_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup
    router_manager.init_router(app)
    await init_db()

    yield
    # on_shutdown


# 创建 FastAPI 应用程序
app = FastAPI(title=CONFIG.app_name, debug=CONFIG.debug, lifespan=lifespan)


# 示例路由
@app.get("/")
def read_root():
    logger.info("Handling root endpoint")
    return {"message": "Welcome to ChenXuBlog!"}


@app.get("/config")
def get_config():
    logger.info("Fetching app configuration")
    return CONFIG.model_dump()


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    logger.info("Testing database connection")
    # 示例：测试数据库连接
    return {"message": "Database connection is working!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
