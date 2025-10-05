from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

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
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
):
    db_comment = CommentDB(
        blog_id=comment.blog_id,
        content=comment.content,
        reply_to_id=comment.reply_to_id,
        user_id=user.id,
    )
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
): ...


@comment.get("/get/{comment_id}", response_model=Comment)
async def get_comment(
    comment_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
): ...


@comment.delete("/delete/{comment_id}")
async def delete_comment(
    comment_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
): ...


@comment.put("/update/{comment_id}")
async def update_comment(
    comment_id: int = Path(..., ge=1),
    comment: CommentCreate = Depends(),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
): ...
