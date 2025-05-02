from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.model.user import User
from backend.schema.auth import LoginResponse, UserLogin
from backend.utils.jwt import create_jwt_token

auth = APIRouter(prefix="/apis/v1/auth", tags=["auth"])


async def get_user_by_evidence(evidence: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.email == evidence))
    if not result:
        pass
    result = await db.execute(select(User).where(User.username == evidence))
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result.scalars().first()


@auth.post("/login", response_model=LoginResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_evidence(user.evidence, db)

    if not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Email or password incorrect")

    jwt_token = create_jwt_token(
        {"sub": str(db_user.uuid), "type": "access"}, timedelta(days=1)
    )

    return LoginResponse(user_uuid=db_user.uuid, access_token=jwt_token)
