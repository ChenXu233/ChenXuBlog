import os
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from .config import CONFIG
from .logger import logger

SQLALCHEMY_DATABASE_URL = CONFIG.DATABASE_URI
DATABASE_URL = Path(CONFIG.DATABASE_URI.split("///")[1])

if not os.path.exists(DATABASE_URL.parent):
    logger.warning(f"数据库目录 {DATABASE_URL.parent} 不存在，正在创建...")
    os.makedirs(DATABASE_URL.parent, exist_ok=True)

# 创建异步引擎
engine: AsyncEngine = create_async_engine(CONFIG.DATABASE_URI)


async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session
        await session.commit()
        await session.close()
