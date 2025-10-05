
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.user import User
from backend.schema.comment import Comment, CommentCreate, CommentsResponse
from backend.utils.jwt import get_access_token_user

comment = APIRouter(prefix="/apis/v1/comment", tags=["comment"])


@comment.post("/create")
async def create_comment(
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_access_token_user),
): ...


@comment.get("/get/{blog_id}", response_model=CommentsResponse)
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
