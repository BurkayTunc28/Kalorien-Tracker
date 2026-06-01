#IntegrityError → Fehler wenn Email schon existiert
#UserCreate → dein Schema (was der User schickt)
#User → dein Model (die Datenbanktabelle)
#SessionDep → die DB-Session
#select → SQL-Abfrage in Python
#HTTPException → Fehler zurückschicken

from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate
from app.models.user import User
from app.database import SessionDep
from sqlmodel import select
from fastapi import HTTPException

#die Daten die der User geschickt hat (email, password)
#konvertiert das Schema in ein Model d.h. aus UserCreate wird ein User-Objekt das in die DB gespeichert werden kann
def create_user(user: UserCreate, session: SessionDep) -> User:
    db_user = User.model_validate(user)
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists.")
    return db_user

#offset=0, limit=100  → erste 100 User
#offset=100, limit=100 → nächste 100 User

def get_users(session: SessionDep, offset: int = 0, limit: int = 100) -> list[User]:

    #select(User)
    # "Ich will alle User aus der Tabelle"
    # SQL: SELECT * FROM user

    # .offset(offset)
    # "Fange bei Eintrag X an"
    # SQL: OFFSET 0

    #.limit(limit)
    # "Gib mir maximal 100"
    # SQL: LIMIT 100

    #session.exec(...)
    # "Führe diese Abfrage aus"
    # schickt das SQL an die Datenbank

    #.all()
    # "Gib mir alle Ergebnisse als Liste"
    # gibt zurück: [User1, User2, User3...]
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

#session.get(User, user_id) sucht direkt per ID
# das ist schneller als select().where() weil die DB direkt per Primary Key sucht
def delete_user(user_id: int, session: SessionDep) -> dict:
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()

    return {"ok": True}


def get_user_by_id(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

