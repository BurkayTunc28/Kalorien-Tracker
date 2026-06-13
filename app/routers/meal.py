from fastapi import APIRouter
from app.services.meal import (
    create_meal as create_meal_service,
    get_meals as get_meal_service,
    delete_meal as delete_meal_service,
    get_daily_meals as get_daily_meals_service
)
from app.schemas.meal import MealPublic, MealCreate
from app.database import SessionDep

router = APIRouter(prefix="/meals", tags=["meals"])

@router.post("/")
def create_meal(meal: MealCreate, session: SessionDep) -> MealPublic:
    return create_meal_service(meal=meal, session=session)

@router.get("/user/{user_id}")
def get_meals(user_id: int, session: SessionDep) -> list[MealPublic]:
    return get_meal_service(user_id=user_id, session=session)

@router.get("/daily/{user_id}")
def get_daily_meals(user_id: int, session: SessionDep) -> dict:
    return get_daily_meals_service(user_id=user_id, session=session)

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, session: SessionDep) -> dict:
    return delete_meal_service(meal_id=meal_id, session=session)