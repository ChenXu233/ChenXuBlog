from typing import List, Optional

from pydantic import BaseModel


class AdminUserResponse(BaseModel):
    id: int
    uuid: str
    username: str
    email: str
    is_verified: bool
    created_at: int
    roles: List[str] = []

    class Config:
        from_attributes = True


class AdminUserListResponse(BaseModel):
    items: List[AdminUserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AdminBlogResponse(BaseModel):
    id: int
    user_uuid: str
    username: str
    title: str
    cover_url: Optional[str]
    tags_name: List[str]
    created_at: int
    updated_at: int
    view_count: int
    likes_count: int
    published: bool

    class Config:
        from_attributes = True


class AdminBlogListResponse(BaseModel):
    items: List[AdminBlogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AdminCommentResponse(BaseModel):
    id: int
    blog_id: int
    blog_title: str
    user_id: str
    username: str
    content: str
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class AdminCommentListResponse(BaseModel):
    items: List[AdminCommentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AdminRoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_default: bool
    permissions: List[str] = []

    class Config:
        from_attributes = True


class AdminStatsResponse(BaseModel):
    total_users: int
    total_blogs: int
    total_comments: int
    total_blogs_today: int
    total_comments_today: int
    recent_blogs: List[AdminBlogResponse] = []
    recent_comments: List[AdminCommentResponse] = []


class UpdateUserRoleRequest(BaseModel):
    role_ids: List[int]
