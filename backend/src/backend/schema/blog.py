from pydantic import BaseModel, Field


class BlogResponse(BaseModel):
    id: int = Field(..., description="Blog id")
    title: str = Field(..., description="Blog title")
    body: str = Field(..., description="Blog body")


class BlogCreate(BaseModel):
    title: str = Field(..., description="Blog title")
    body: str = Field(..., description="Blog body")
    published: bool = Field(..., description="Blog published status")

    class Config:
        orm_mode = True


class BlogUpdate(BaseModel):
    title: str = Field(..., description="Blog title")
    body: str = Field(..., description="Blog body")
    published: bool = Field(..., description="Blog published status")

    class Config:
        orm_mode = True
