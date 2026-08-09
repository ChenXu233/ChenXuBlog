"""分页工具类：统一分页计算逻辑。"""
from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PageParams(BaseModel):
    """分页请求参数。"""

    page: int = 1
    page_size: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def total_pages(self, total: int) -> int:
        return ceil(total / self.page_size) if total > 0 else 1


class PageResult(BaseModel, Generic[T]):
    """分页响应结构。"""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def build(cls, items: list[T], total: int, page: int, page_size: int) -> "PageResult[T]":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=ceil(total / page_size) if total > 0 else 1,
        )


def paginate(page: int, page_size: int, total: int) -> tuple[int, int, int]:
    """计算 offset 和 total_pages。

    返回 (offset, total_pages, safe_page)
    """
    safe_page = max(page, 1)
    safe_size = max(min(page_size, 100), 1)
    total_pages = ceil(total / safe_size) if total > 0 else 1
    return (safe_page - 1) * safe_size, total_pages, safe_page
