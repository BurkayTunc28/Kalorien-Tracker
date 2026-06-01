from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.database import SessionDep
from app.services.auth import decode_token
from app.services.user import get_user_by_id


def token_auth(
        session: SessionDep,
        access_token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    decoded_access_token = decode_token(access_token.credentials)
    user_id = decoded_access_token["userId"]
    user = get_user_by_id(user_id, session)
    return user