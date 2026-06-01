from app.models.user import User
from app.database import SessionDep
from sqlmodel import select
from fastapi import HTTPException
import jwt

from app.schemas.jwt import JwtPublic

jwt_secret = "sgasdgadsdfhödafj244690z*ç55/_:;,igf"
jwt_algorithm = "HS256"

def authenticate_user(email: str, password: str, session: SessionDep) -> User:
    db_user = session.exec(select(User).where(User.email == email)).first()
    if not db_user or not db_user.password == password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return db_user

def create_jwt(user: User) -> JwtPublic:
    jwt_payload = {"userId": user.id}
    encoded_jwt = jwt.encode(jwt_payload, jwt_secret, algorithm=jwt_algorithm)
    return JwtPublic(access_token=encoded_jwt)

def decode_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        return decoded
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")