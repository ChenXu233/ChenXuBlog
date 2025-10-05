from typing import List, Optional

from pydantic import BaseModel, Field


class BlogResponse(BaseModel):
    id: int = Field(..., description="Blog id")
    user_uuid: str = Field(..., description="User UUID")
    title: str = Field(..., description="Blog title")
    headShot: Optional[str] = Field(..., description="Blog headshot")
    body: str = Field(..., description="Blog body")
    tags_name: List[str] = Field(..., description="Blog tags")
    created_at: int = Field(..., description="Blog creation time")
    updated_at: int = Field(..., description="Blog update time")
    view_count: int = Field(..., description="Blog view count")
    likes_count: int = Field(..., description="Blog like count")
    published: bool = Field(..., description="Blog published status")
    like: int = Field(..., description="Blog like count")

    class Config:
        from_attributes = True


class BlogCreate(BaseModel):
    title: str = Field(..., description="Blog title")
    body: str = Field(..., description="Blog body")
    tags: list[str] = Field(..., description="Blog tags")
    published: bool = Field(..., description="Blog published status")

    class Config:
        from_attributes = True


class BlogUpdate(BaseModel):
    title: str = Field(..., description="Blog title")
    body: str = Field(..., description="Blog body")
    tags: list[str] = Field(..., description="Blog tags")
    published: bool = Field(..., description="Blog published status")

    class Config:
        from_attributes = True
