#FoodCreate → dein Schema (was der Food schickt)
#Food → dein Model (die Datenbanktabelle)
#SessionDep → die DB-Session
#select → SQL-Abfrage in Python
#HTTPException → Fehler zurückschicken

from app.models.meal import Meal
from app.schemas.meal import MealCreate
from app.database import SessionDep
from app.services.food import get_food_by_id
from app.services.profile import get_profile
from sqlmodel import select
from fastapi import HTTPException
from datetime import date

#die Daten die Meal geschickt hat (name, calories, protein etc.)
#konvertiert das Schema in ein Model d.h. aus MealCreate wird ein Meal-Objekt das in die DB gespeichert werden kann
def create_meal(meal: MealCreate, session: SessionDep) -> Meal:
    #1. Lebensmittel aus DB holen
    food = get_food_by_id(meal.food_id, session)

    # 2. Kalorien berechnen
    # Kalorien berechnen basierend auf der Referenzmenge des Lebensmittels
    # Beispiel: menge=200g, food.kalorien=165 bei referenz_menge=100g
    # kalorien = (200 / 100) * 165 = 330 kcal
    kalorien = (meal.menge / food.menge_gramm) * food.kalorien

      # 3. Meal-Objekt erstellen mit berechneten Kalorien
    db_meal = Meal(name=meal.name, user_id = meal.user_id, food_id = meal.food_id, menge = meal.menge, kalorien = round(kalorien, 2))

    session.add(db_meal)
    session.commit()
    session.refresh(db_meal)
    return db_meal

def get_meals(user_id: int, session: SessionDep) -> list[Meal]:
    # Nur Mahlzeiten DIESES Users holen
    meals = session.exec(select(Meal).where(Meal.user_id == user_id)).all()
    return meals

def get_daily_meals(user_id: int, session: SessionDep) -> dict:
    # Kalorienziel aus dem Profil holen
    profile = get_profile(user_id, session)
    kalorienziel = profile.kalorienziel
    
    heute = date.today()
    meals = session.exec(select(Meal).where(Meal.user_id == user_id,)).all()
    
    meals_heute = []
    for m in meals:
        if m.created_at.date() == heute:
            meals_heute.append(m)
    
    gesamtkalorien = sum(m.kalorien for m in meals_heute)
    noch_uebrig = kalorienziel - gesamtkalorien
    
    return {
        "datum": str(heute),
        "gesamtkalorien_heute": round(gesamtkalorien, 2),
        "kalorienziel": round(kalorienziel, 2),
        "noch_uebrig": round(noch_uebrig, 2)
    }

def delete_meal(meal_id: int, session: SessionDep) -> dict:
    meal = session.get(Meal, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    session.delete(meal)
    session.commit()
    return {"ok": True}


