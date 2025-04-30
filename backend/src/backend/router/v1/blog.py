from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.blog import Blog, Tag
from backend.model.user import User
from backend.schema.blog import BlogCreate, BlogResponse
from backend.utils.jwt import get_jwt_token_user

blog = APIRouter(prefix="/apis/v1/blog", tags=["blog"])


@blog.get("/{id}", response_model=BlogResponse)
async def get_blog(
    id: int = Path(..., gt=0),
    token: Optional[str] = Header(default=None, description="JWT Token"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(Blog.select().where(Blog.id == id))
    blog: Optional[Blog] = result.scalars().first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if token:
        try:
            user = await get_jwt_token_user(token)
            if blog.user_uuid != user.uuid and not blog.published:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to view this blog",
                )
            return blog.to_ResponseModel()
        except HTTPException as e:
            if e.status_code == 403:
                raise e

    if not blog.published:
        raise HTTPException(status_code=403, detail="This blog is not published yet")

    return blog.to_ResponseModel()


@blog.post("/", response_model=BlogResponse)
async def create_blog(
    blog: BlogCreate,
    user: User = Depends(get_jwt_token_user),
    db: AsyncSession = Depends(get_db),
):
    new_blog = Blog(
        user_uuid=user.uuid,
        user=user,
        title=blog.title,
        body=blog.body,
        published=blog.published,
    )

    for tag_name in blog.tags:
        tag = await db.execute(Tag.select().where(Tag.name == tag_name))
        if not tag.scalar():
            tag = Tag(name=tag_name)
            db.add(tag)
        new_blog.tags.append(tag)

    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog.to_ResponseModel()
