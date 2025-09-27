from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.model.blog import Blog, Tag
from backend.model.user import User
from backend.schema.blog import BlogCreate, BlogResponse
from backend.utils.jwt import get_access_token_user

blog = APIRouter(prefix="/apis/v1/blog", tags=["blog"])


@blog.get("/{id}", response_model=BlogResponse)
async def get_blog(
    id: int = Path(..., gt=0),
    token: str | None = Header(None, description="Access Token"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Blog).where(Blog.id == id).options(selectinload(Blog.tags))
    )
    db_blog: Optional[Blog] = result.scalars().first()

    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if token:
        user = await get_access_token_user(token, db)
        if db_blog.user_uuid != user.uuid and not db_blog.published:
            raise HTTPException(
                status_code=403, detail="You do not have permission to view this blog"
            )

    if not db_blog.published:
        raise HTTPException(status_code=403, detail="This blog is not published yet")

    db_blog.view_count += 1
    await db.commit()

    return await db_blog.to_ResponseModel(db)


@blog.post("/{id}", response_model=BlogResponse)
async def update_blog(
    blog: BlogCreate,
    id: int = Path(..., gt=0),
    user: User = Depends(get_access_token_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Blog).where(Blog.id == id))
    db_blog: Optional[Blog] = result.scalars().first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if db_blog.user_uuid != user.uuid:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this blog"
        )

    db_blog.title = blog.title
    db_blog.body = blog.body
    db_blog.published = blog.published
    db_blog.updated_at = datetime.now()

    for tag_name in blog.tags:
        tag = await db.execute(Tag.select().where(Tag.name == tag_name))
        if not tag.scalar():
            tag = Tag(name=tag_name)
            db.add(tag)
        db_blog.tags.append(tag)

    await db.commit()
    return await db_blog.to_ResponseModel(db)


@blog.post("/", response_model=BlogResponse)
async def create_blog(
    blog: BlogCreate,
    user: User = Depends(get_access_token_user),
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
    return await new_blog.to_ResponseModel(db)
