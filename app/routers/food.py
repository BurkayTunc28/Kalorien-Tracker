from fastapi import APIRouter, Depends
from app.models.food import Food
from app.services.food import (
    create_food as create_food_service,
    get_foods as get_foods_service,
    delete_food as delete_food_service,
    get_food_by_id as get_food_by_id_service
)
from app.schemas.food import FoodPublic, FoodCreate
from app.database import SessionDep
from typing import Annotated
from fastapi import Query

router = APIRouter(prefix="/foods", tags=["foods"])

@router.post("/")
def create_food(food: FoodCreate, session: SessionDep) -> FoodPublic:
    return create_food_service(food=food, session=session)


@router.get("/")
def get_foods(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,) -> list[FoodPublic]:
    return get_foods_service(session=session, offset=offset, limit=limit)


@router.get("/{food_id}")
def get_food(food_id: int, session: SessionDep) -> FoodPublic:
    return get_food_by_id_service(food_id=food_id, session=session)


@router.delete("/{food_id}")
def delete_food(food_id: int, session: SessionDep) -> dict:
    return delete_food_service(food_id=food_id, session=session)