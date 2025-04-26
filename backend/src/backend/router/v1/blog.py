from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.blog import Blog
from backend.schema.blog import BlogCreate, BlogResponse

blog = APIRouter(prefix="/apis/v1/blog", tags=["blog"])


@blog.get("/{id}", response_model=BlogResponse)
async def get_blog(
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(Blog.select().where(Blog.id == id))
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


@blog.post("/", response_model=BlogResponse)
async def create_blog(
    blog: BlogCreate,
    db: AsyncSession = Depends(get_db),
):
    new_blog = Blog(
        title=blog.title,
        body=blog.body,
        published=blog.published,
    )
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog
