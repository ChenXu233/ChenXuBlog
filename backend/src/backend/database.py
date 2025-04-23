import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import CONFIG
from .logger import logger

SQLALCHEMY_DATABASE_URL = CONFIG.database_url
DATABASE_URL = Path(CONFIG.database_url.split("///")[1])

if not os.path.exists(DATABASE_URL.parent):
    logger.warning(f"数据库目录 {DATABASE_URL.parent} 不存在，正在创建...")
    os.makedirs(DATABASE_URL.parent, exist_ok=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
    ),
)

Session = sessionmaker(bind=engine)

Base = declarative_base()


# 数据库初始化函数（可选）
def init_db():
    """
    初始化数据库。
    """
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"数据库初始化失败: {e}")


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
