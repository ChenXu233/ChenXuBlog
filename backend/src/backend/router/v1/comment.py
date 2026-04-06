from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.model.comment import Comment as CommentDB
from backend.model.user import User
from backend.schema.comment import Comment, CommentCreate, CommentsResponse
from backend.utils.jwt import get_access_token_user
from backend.utils.permission import require_permissions

comment = APIRouter(prefix="/apis/v1/comment", tags=["comment"])


@comment.post(
    "/create",
    name="create_comment",
    response_model=Comment,
    dependencies=[Depends(require_permissions("comment:create", "create comment"))],
)
async def create_comment(
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    parent_comment = None
    if comment_data.reply_to_id:
        result = await db.execute(
            select(CommentDB).where(CommentDB.id == comment_data.reply_to_id)
        )
        parent_comment = result.scalars().first()
        if not parent_comment:
            raise HTTPException(status_code=404, detail="Parent comment not found")

    db_comment = CommentDB(
        blog_id=comment_data.blog_id,
        content=comment_data.content,
        user_id=user.id,
    )
    if parent_comment:
        db_comment.parent = parent_comment

    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


@comment.get(
    "/get/{blog_id}",
    name="get_comments",
    response_model=CommentsResponse,
    dependencies=[Depends(require_permissions("comment:read", "read comment"))],
)
async def get_comments(
    blog_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    # 获取顶级评论（没有父评论的评论）
    result = await db.execute(
        select(CommentDB)
        .where(CommentDB.blog_id == blog_id, CommentDB.parent.is_(None))
        .options(selectinload(CommentDB.replies))
        .order_by(CommentDB.created_at.desc())
    )
    comments = result.scalars().all()

    # 转换为响应格式
    comment_list = []
    for c in comments:
        comment_list.append(Comment.model_validate(c))
        # 添加回复
        for reply in c.replies:
            comment_list.append(Comment.model_validate(reply))

    return CommentsResponse(comments=comment_list, total=len(comment_list))


@comment.get("/get/{comment_id}", response_model=Comment)
async def get_comment(
    comment_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    result = await db.execute(select(CommentDB).where(CommentDB.id == comment_id))
    db_comment = result.scalars().first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return db_comment


@comment.delete("/delete/{comment_id}")
async def delete_comment(
    comment_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    result = await db.execute(select(CommentDB).where(CommentDB.id == comment_id))
    db_comment = result.scalars().first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 检查是否是评论所有者
    if db_comment.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="You can only delete your own comments"
        )

    await db.delete(db_comment)
    await db.commit()

    return {"message": "Comment deleted successfully"}


@comment.put("/update/{comment_id}")
async def update_comment(
    comment_id: int = Path(..., ge=1),
    comment_data: CommentCreate = Depends(),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    result = await db.execute(select(CommentDB).where(CommentDB.id == comment_id))
    db_comment = result.scalars().first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 检查是否是评论所有者
    if db_comment.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="You can only update your own comments"
        )

    db_comment.content = comment_data.content
    db_comment.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(db_comment)

    return db_comment
