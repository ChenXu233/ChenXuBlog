from math import ceil
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.model.blog import Blog
from backend.model.comment import Comment as CommentDB
from backend.model.user import Role, User
from backend.schema.admin import (
    AdminBlogListResponse,
    AdminBlogResponse,
    AdminCommentListResponse,
    AdminCommentResponse,
    AdminRoleResponse,
    AdminStatsResponse,
    AdminUserListResponse,
    AdminUserResponse,
    UpdateUserRoleRequest,
)
from backend.utils.jwt import get_access_token_user
from backend.utils.permission import require_permissions

admin = APIRouter(prefix="/apis/v1/admin", tags=["admin"])


def user_to_response(user: User) -> AdminUserResponse:
    return AdminUserResponse(
        id=user.id,
        uuid=user.uuid,
        username=user.username,
        email=user.email,
        is_verified=user.is_verified,
        created_at=int(user.created_at.timestamp()),
        roles=[r.name for r in user.roles],
    )


def blog_to_response(blog: Blog, username: str = "") -> AdminBlogResponse:
    return AdminBlogResponse(
        id=blog.id,
        user_uuid=blog.user_uuid,
        username=username or (blog.user.username if blog.user else ""),
        title=blog.title,
        cover_url=blog.cover_url,
        tags_name=[t.name for t in blog.tags] if blog.tags else [],
        created_at=int(blog.created_at.timestamp()),
        updated_at=int(blog.updated_at.timestamp()),
        view_count=blog.view_count,
        likes_count=blog.likes_count,
        published=blog.published,
    )


def comment_to_response(comment: CommentDB, blog_title: str = "", username: str = "") -> AdminCommentResponse:
    return AdminCommentResponse(
        id=comment.id,
        blog_id=comment.blog_id,
        blog_title=blog_title or (comment.blog.title if comment.blog else ""),
        user_id=comment.user_id,
        username=username or (comment.user.username if comment.user else ""),
        content=comment.content,
        created_at=int(comment.created_at.timestamp()),
        updated_at=int(comment.updated_at.timestamp()) if comment.updated_at else 0,
    )


def admin_dependency():
    return Depends(
        require_permissions(
            required_permission="admin:access",
            permission_description="Access admin dashboard",
        )
    )


@admin.get("/stats", response_model=AdminStatsResponse)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """获取仪表盘统计数据"""
    # 用户总数
    total_users = (await db.execute(select(func.count()).select_from(User))).scalar() or 0

    # 文章总数
    total_blogs = (await db.execute(select(func.count()).select_from(Blog))).scalar() or 0

    # 评论总数
    total_comments = (await db.execute(select(func.count()).select_from(CommentDB))).scalar() or 0

    # 今日新增文章
    from datetime import datetime, timezone
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    total_blogs_today = (
        await db.execute(select(func.count()).select_from(Blog).where(Blog.created_at >= today_start))
    ).scalar() or 0

    # 今日新增评论
    total_comments_today = (
        await db.execute(select(func.count()).select_from(CommentDB).where(CommentDB.created_at >= today_start))
    ).scalar() or 0

    # 最近5篇文章
    recent_blogs_query = (
        select(Blog)
        .options(selectinload(Blog.tags), selectinload(Blog.user))
        .order_by(Blog.created_at.desc())
        .limit(5)
    )
    recent_blogs_result = await db.execute(recent_blogs_query)
    recent_blogs = [blog_to_response(b) for b in recent_blogs_result.scalars().all()]

    # 最近5条评论
    recent_comments_query = (
        select(CommentDB)
        .options(selectinload(CommentDB.blog), selectinload(CommentDB.user))
        .order_by(CommentDB.created_at.desc())
        .limit(5)
    )
    recent_comments_result = await db.execute(recent_comments_query)
    recent_comments = [comment_to_response(c) for c in recent_comments_result.scalars().all()]

    return AdminStatsResponse(
        total_users=total_users,
        total_blogs=total_blogs,
        total_comments=total_comments,
        total_blogs_today=total_blogs_today,
        total_comments_today=total_comments_today,
        recent_blogs=recent_blogs,
        recent_comments=recent_comments,
    )


@admin.get("/users", response_model=AdminUserListResponse)
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """获取用户列表"""
    # 获取总数
    total = (await db.execute(select(func.count()).select_from(User))).scalar() or 0
    total_pages = ceil(total / page_size) if total > 0 else 1

    # 分页查询
    offset = (page - 1) * page_size
    query = (
        select(User)
        .options(selectinload(User.roles))
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    users = result.scalars().all()

    return AdminUserListResponse(
        items=[user_to_response(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@admin.put("/users/{user_id}/role", response_model=AdminUserResponse)
async def update_user_roles(
    req: UpdateUserRoleRequest,
    user_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """更新用户角色"""
    # 获取目标用户
    result = await db.execute(select(User).where(User.id == user_id).options(selectinload(User.roles)))
    target_user = result.scalars().first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 获取角色
    roles_result = await db.execute(select(Role).where(Role.id.in_(req.role_ids)))
    roles = roles_result.scalars().all()

    # 更新角色
    target_user.roles = list(roles)
    await db.commit()
    await db.refresh(target_user)

    return user_to_response(target_user)


@admin.delete("/users/{user_id}")
async def delete_user(
    user_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    """删除用户"""
    if user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    result = await db.execute(select(User).where(User.id == user_id))
    target_user = result.scalars().first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(target_user)
    await db.commit()
    return {"message": "User deleted successfully"}


@admin.get("/blogs", response_model=AdminBlogListResponse)
async def get_blogs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    published: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """获取文章列表(包含未发布的)"""
    query = select(Blog).options(selectinload(Blog.tags), selectinload(Blog.user))

    if published is not None:
        query = query.where(Blog.published == published)

    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    total_pages = ceil(total / page_size) if total > 0 else 1

    # 分页
    offset = (page - 1) * page_size
    query = query.order_by(Blog.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    blogs = result.scalars().all()

    return AdminBlogListResponse(
        items=[blog_to_response(b) for b in blogs],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@admin.put("/blogs/{blog_id}/publish")
async def toggle_blog_publish(
    blog_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """切换文章发布状态"""
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.published = not blog.published
    await db.commit()
    return {"published": blog.published}


@admin.delete("/blogs/{blog_id}")
async def delete_blog(
    blog_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """删除文章"""
    result = await db.execute(select(Blog).where(Blog.id == blog_id))
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    await db.delete(blog)
    await db.commit()
    return {"message": "Blog deleted successfully"}


@admin.get("/comments", response_model=AdminCommentListResponse)
async def get_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """获取评论列表"""
    # 获取总数
    total = (await db.execute(select(func.count()).select_from(CommentDB))).scalar() or 0
    total_pages = ceil(total / page_size) if total > 0 else 1

    # 分页查询
    offset = (page - 1) * page_size
    query = (
        select(CommentDB)
        .options(selectinload(CommentDB.blog), selectinload(CommentDB.user))
        .order_by(CommentDB.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    comments = result.scalars().all()

    return AdminCommentListResponse(
        items=[comment_to_response(c) for c in comments],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@admin.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """删除评论"""
    result = await db.execute(select(CommentDB).where(CommentDB.id == comment_id))
    comment = result.scalars().first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    await db.delete(comment)
    await db.commit()
    return {"message": "Comment deleted successfully"}


@admin.get("/roles", response_model=list[AdminRoleResponse])
async def get_roles(
    db: AsyncSession = Depends(get_db),
    _: User = admin_dependency(),
):
    """获取所有角色"""
    result = await db.execute(select(Role).options(selectinload(Role.permissions)))
    roles = result.scalars().all()

    return [
        AdminRoleResponse(
            id=r.id,
            name=r.name,
            description=r.description,
            is_default=r.is_default,
            permissions=[p.code for p in r.permissions],
        )
        for r in roles
    ]
