#IntegrityError → Fehler wenn Email schon existiert
#FoodCreate → dein Schema (was der Food schickt)
#Food → dein Model (die Datenbanktabelle)
#SessionDep → die DB-Session
#select → SQL-Abfrage in Python
#HTTPException → Fehler zurückschicken

from flask import session

from app.models.food import Food
from app.schemas.food import FoodCreate
from app.database import SessionDep
from sqlmodel import select
from fastapi import HTTPException

#die Daten die Food geschickt hat (name, calories, protein etc.)
#konvertiert das Schema in ein Model d.h. aus FoodCreate wird ein Food-Objekt das in die DB gespeichert werden kann
def create_food(food: FoodCreate, session: SessionDep) -> Food:
    db_food = Food.model_validate(food)
    session.add(db_food)
    session.commit()
    session.refresh(db_food)
    return db_food

#offset=0, limit=100  → erste 100 User
#offset=100, limit=100 → nächste 100 User

def get_foods(session: SessionDep, offset: int = 0, limit: int = 100) -> list[Food]:
    foods = session.exec(select(Food).offset(offset).limit(limit)).all()
    return foods


def get_food_by_id(food_id: int, session: SessionDep) -> Food:
    # Sucht direkt per ID - schneller als select().where()
    food = session.get(Food, food_id)
    
    # Wenn kein Lebensmittel mit dieser ID gefunden wird
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    return food

#session.get(Food, food_id) sucht direkt per ID
# das ist schneller als select().where() weil die DB direkt per Primary Key sucht
def delete_food(food_id: int, session: SessionDep) -> dict:
    food = session.get(Food, food_id)

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    session.delete(food)
    session.commit()

    return {"ok": True}


