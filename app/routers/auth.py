from fastapi import APIRouter
from app.database import SessionDep
from app.schemas.jwt import JwtPublic
from app.schemas.user import UserAuth
from app.services.auth import authenticate_user, create_jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=JwtPublic)
def login(user: UserAuth, session: SessionDep):
    db_user = authenticate_user(user.email, user.password, session)
    return create_jwt(db_user)