from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.logger import logger

from .config import CONFIG
from .database import init_db
from .router import router_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup
    router_manager.init_router(app)
    await init_db()

    yield
    # on_shutdown


app = FastAPI(title=CONFIG.APP_NAME, debug=CONFIG.DEBUG, lifespan=lifespan)


# 示例路由
@app.get("/")
def read_root():
    logger.info("Handling root endpoint")
    return {"message": "Welcome to ChenXuBlog!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
