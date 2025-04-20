from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .logger import logger, setup_fastapi_logger
from .database import init_db, get_db
from .config import CONFIG

setup_fastapi_logger()

init_db()

app = FastAPI(title=CONFIG.app_name, debug=CONFIG.debug)


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
