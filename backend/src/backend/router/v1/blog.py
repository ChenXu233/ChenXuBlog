from datetime import datetime, timezone
from math import ceil
from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Path, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.model.blog import Blog, Tag
from backend.model.user import User
from backend.schema.blog import BlogCreate, BlogListResponse, BlogResponse
from backend.utils.jwt import get_access_token_user, get_access_token_user_uuid
from backend.utils.permission import require_permissions

blog = APIRouter(prefix="/apis/v1/blog", tags=["blog"])


@blog.get("/", response_model=BlogListResponse)
async def get_blogs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    search: Optional[str] = Query(None, description="Search in title and body"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Blog).where(Blog.published == True)

    if tag:
        query = query.join(Blog.tags).where(Tag.name == tag)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(Blog.title.like(search_pattern), Blog.body.like(search_pattern))
        )

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    total_pages = ceil(total / page_size) if total > 0 else 1
    offset = (page - 1) * page_size

    query = query.options(selectinload(Blog.tags), selectinload(Blog.like))
    query = query.order_by(Blog.created_at.desc()).offset(offset).limit(page_size)

    result = await db.execute(query)
    blogs = result.unique().scalars().all()

    items = []
    for b in blogs:
        items.append(await b.to_ResponseModel(db))

    return BlogListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@blog.get("/{id}", response_model=BlogResponse)
async def get_blog(
    id: int = Path(..., gt=0),
    authorization: str | None = Header(None, alias="Authorization"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Blog).where(Blog.id == id).options(selectinload(Blog.tags), selectinload(Blog.like))
    )
    db_blog: Optional[Blog] = result.unique().scalars().first()

    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if authorization and authorization.startswith("Bearer "):
        try:
            user_uuid = get_access_token_user_uuid(authorization)
            if db_blog.user_uuid != user_uuid and not db_blog.published:
                raise HTTPException(
                    status_code=403, detail="You do not have permission to view this blog"
                )
        except HTTPException:
            pass

    if not db_blog.published:
        raise HTTPException(status_code=403, detail="This blog is not published yet")

    db_blog.view_count += 1
    await db.commit()

    return await db_blog.to_ResponseModel(db)


@blog.put(
    "/{id}",
    response_model=BlogResponse,
    dependencies=[
        Depends(
            require_permissions(
                required_permission="blog:update", permission_description="Update blog"
            )
        )
    ],
)
async def update_blog(
    blog: BlogCreate,
    id: int = Path(..., gt=0),
    user: User = Depends(get_access_token_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Blog).where(Blog.id == id).options(selectinload(Blog.tags), selectinload(Blog.like)))
    db_blog: Optional[Blog] = result.unique().scalars().first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if db_blog.user_uuid != user.uuid:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this blog"
        )

    db_blog.title = blog.title
    db_blog.body = blog.body
    db_blog.published = blog.published
    db_blog.updated_at = datetime.now(timezone.utc)

    # Clear existing tags first
    db_blog.tags = []
    for tag_name in blog.tags:
        tag = await db.execute(select(Tag).where(Tag.name == tag_name))
        existing = tag.scalar_one_or_none()
        if not existing:
            existing = Tag(name=tag_name)
            db.add(existing)
        db_blog.tags.append(existing)

    await db.commit()
    await db.refresh(db_blog, ["tags", "like"])
    return BlogResponse(
        id=db_blog.id,
        user_uuid=db_blog.user_uuid,
        title=db_blog.title,
        cover_url=db_blog.cover_url,
        body=db_blog.body,
        tags_name=[t.name for t in (db_blog.tags or [])],
        created_at=db_blog.created_at,
        updated_at=db_blog.updated_at,
        view_count=db_blog.view_count,
        likes_count=len(db_blog.like or []),
        published=db_blog.published,
    )


@blog.post(
    "/",
    response_model=BlogResponse,
    dependencies=[
        Depends(
            require_permissions(
                required_permission="blog:create", permission_description="Create blog"
            )
        )
    ],
)
async def create_blog(
    blog: BlogCreate,
    user: User = Depends(get_access_token_user),
    db: AsyncSession = Depends(get_db),
):
    new_blog = Blog(
        user_uuid=user.uuid,
        title=blog.title,
        body=blog.body,
        published=blog.published,
    )

    for tag_name in blog.tags:
        tag = await db.execute(select(Tag).where(Tag.name == tag_name))
        if not tag.scalar():
            tag = Tag(name=tag_name)
            db.add(tag)
        new_blog.tags.append(tag)

    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog, ["tags", "like"])
    return await new_blog.to_ResponseModel(db)


@blog.delete(
    "/{id}",
    dependencies=[
        Depends(
            require_permissions(
                required_permission="blog:delete", permission_description="Delete blog"
            )
        )
    ],
)
async def delete_blog(
    id: int = Path(..., gt=0),
    user: User = Depends(get_access_token_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Blog).where(Blog.id == id).options(selectinload(Blog.like)))
    db_blog: Optional[Blog] = result.unique().scalars().first()

    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if db_blog.user_uuid != user.uuid:
        raise HTTPException(
            status_code=403, detail="You do not have permission to delete this blog"
        )

    await db.delete(db_blog)
    await db.commit()

    return {"message": "Blog deleted successfully"}


@blog.post("/{id}/like", name="toggle_like")
async def toggle_like(
    id: int = Path(..., gt=0),
    user: User = Depends(get_access_token_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Blog).where(Blog.id == id).options(selectinload(Blog.like))
    )
    db_blog: Optional[Blog] = result.unique().scalars().first()

    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    liked = any(u.uuid == user.uuid for u in (db_blog.like or []))

    if liked:
        db_blog.like = [u for u in (db_blog.like or []) if u.uuid != user.uuid]
        message = "Like removed"
    else:
        db_blog.like.append(user)
        message = "Like added"

    await db.commit()
    await db.refresh(db_blog, ["like"])
    return {"liked": not liked, "likes_count": len(db_blog.like or []), "message": message}


@blog.get("/{id}/like", name="get_like_status")
async def get_like_status(
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Blog).where(Blog.id == id).options(selectinload(Blog.like))
    )
    db_blog: Optional[Blog] = result.unique().scalars().first()

    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"likes_count": len(db_blog.like)}