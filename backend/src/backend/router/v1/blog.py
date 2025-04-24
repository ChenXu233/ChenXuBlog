from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.blog import Blog
from backend.schema.blog import BlogResponse

blog = APIRouter(prefix="/apis/v1/blog", tags=["blog"])


@blog.get("/{id}", response_model=BlogResponse)
async def get_blog(
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(Blog.__table__.select().where(Blog.id == id))
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog
