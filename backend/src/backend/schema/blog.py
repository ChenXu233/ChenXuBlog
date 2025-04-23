from pydantic import BaseModel, Field


class BlogResponse(BaseModel):
    id: int = Field(..., description="Blog id")
    title: str = Field(..., description="Blog title")
    body: str = Field(..., description="Blog body")
