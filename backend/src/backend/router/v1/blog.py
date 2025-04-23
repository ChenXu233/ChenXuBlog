from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schema.blog import BlogResponse

blog = APIRouter(prefix="/apis/v1/blog", tags=["blog"])


@blog.get("/{id}", response_model=BlogResponse)
async def get_blog(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    ...
