from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CommentCreate(BaseModel):
    blog_id: int
    content: str
    reply_to_id: Optional[int] = None


class Comment(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    blog_id: int
    reply_to_id: Optional[int] = None

    class Config:
        from_attributes = True


class CommentsResponse(BaseModel):
    comments: List[Comment] = []
    total: int = 0

    class Config:
        from_attributes = True
