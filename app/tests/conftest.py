from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import SQLModel, create_engine, Session
from app.database import get_session
from pytest import fixture

from app.models.user import User
from app.models.food import Food
from app.models.profile import Profile
from app.models.meal import Meal
from app.services.auth import create_jwt
from app.services.profile import create_profile
from app.schemas.profile import ProfileCreate
from app.services.profile import berechne_bmr, berechne_gsu



@fixture
def db():
    sqlite_file_name = "database_test.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    return Session(engine)

@fixture
def client(db):
    return TestClient(app)

#erstellter User
@fixture
def user_burkay(db) -> User:
    user = User(email="burkay@test.ch", password="1234")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#Food Item 1
@fixture
def food_poulet(db) -> Food:
    food = Food(name="Poulet", menge_gramm=100, kalorien=165, protein=31, kohlenhydrate=0, fett=3.6)
    db.add(food)
    db.commit()
    db.refresh(food)
    return food

#Food Item 1
@fixture
def food_reis(db) -> Food:
    food = Food(name="Reis", menge_gramm=100, kalorien=130, protein=2.7, kohlenhydrate=28, fett=0.3)
    db.add(food)
    db.commit()
    db.refresh(food)
    return food

# Profil für Burkay mit BMR- und GSU-Berechnung
@fixture
def profile_burkay(db, user_burkay) -> Profile:
    profile_data = ProfileCreate(
        user_id=user_burkay.id,
        gewicht=110,
        zielgewicht=90,
        groesse=172,
        alter=27,
        geschlecht="m",
        aktivitaet=1
    )
    return create_profile(profile_data, db)

# Rohdaten für ein Profil - werden sowohl zum POST-Request als auch zur Berechnung der Erwartungswerte im Test genutzt
@fixture
def profile_burkay_daten(user_burkay) -> dict:
    return {
        "user_id": user_burkay.id,
        "gewicht": 110,
        "zielgewicht": 90,
        "groesse": 172,
        "alter": 26,
        "geschlecht": "m",
        "aktivitaet": 1
    }

# Berechnet das erwartete kalorienziel aus profile_burkay_daten mit denselben Funktionen wie services/profile.py
@fixture
def erwartetes_kalorienziel(profile_burkay_daten) -> float:
    bmr = berechne_bmr(
        profile_burkay_daten["gewicht"],
        profile_burkay_daten["groesse"],
        profile_burkay_daten["alter"],
        profile_burkay_daten["geschlecht"]
    )
    gsu = berechne_gsu(bmr, profile_burkay_daten["aktivitaet"])
    return round(gsu - (gsu * 0.15), 2)

# Mahlzeit für Burkay (200g Poulet)
@fixture
def meal_burkay(db, user_burkay, food_poulet) -> Meal:
    meal = Meal(
        user_id=user_burkay.id,
        food_id=food_poulet.id,
        menge=200,
        kalorien=330.0,
        name="Mittagessen"
    )
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

# Zweite Mahlzeit für Burkay (z.B. 100g Reis)
@fixture
def meal_burkay_2(db, user_burkay, food_reis) -> Meal:
    meal = Meal(
        user_id=user_burkay.id,
        food_id=food_reis.id,
        menge=100,
        kalorien=130.0,  # (100/100) * 130
        name="Abendessen"
    )
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

#user mit auth token
@fixture
def client_burkay(client, user_burkay):
    access_token = create_jwt(user_burkay).access_token
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client


