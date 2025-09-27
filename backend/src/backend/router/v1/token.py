
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schema.token import TokenResponse
from backend.utils.jwt import generate_access_token, get_refresh_token_user

token = APIRouter(prefix="/apis/v1/token", tags=["token"])


@token.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Refresh token not found")
    user = await get_refresh_token_user(refresh_token, db)
    token = generate_access_token(user.uuid)
    return TokenResponse(token=token)
