import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import CONFIG

SQLALCHEMY_DATABASE_URL = CONFIG.database_url
DATABASE_URL = Path(CONFIG.database_url.split("///")[1])

if not os.path.exists(DATABASE_URL.parent):
    os.makedirs(DATABASE_URL.parent, exist_ok=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    if "sqlite" in SQLALCHEMY_DATABASE_URL
    else {},
)

SessionLocal = sessionmaker(bind=engine)

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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
