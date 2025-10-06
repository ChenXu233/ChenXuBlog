from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.logger import logger

from .config import CONFIG
from .database import get_db, init_db
from .router import router_manager
from .utils.first_start import check_is_first_start, first_start
from .utils.permission import permission_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup
    logger.info("Application startup")
    router_manager.init_router(app)
    await init_db()

    async for db in get_db():
        await permission_manager.update_permission_db(db)
        if await check_is_first_start(db):
            await first_start(db)

    logger.info("Application startup completed")

    yield
    # on_shutdown


app = FastAPI(title=CONFIG.APP_NAME, debug=CONFIG.DEBUG, lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 示例路由
@app.get("/")
def read_root():
    logger.info("Handling root endpoint")
    return {"message": "Welcome to ChenXuBlog!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
