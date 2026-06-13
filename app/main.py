#Ein Python-Werkzeug für Lifespan-Events — Dinge die beim Start und Ende der App passieren sollen.
from contextlib import asynccontextmanager
#Das FastAPI-Framework selbst, damit erstellst man die App.
from fastapi import FastAPI

#Die Funktion die beim Start alle Tabellen in der DB erstellt
from app.database import create_db_and_tables


from app.routers.user import router as user_router
from app.routers.meal import router as meal_router
from app.routers.profile import router as profile_router
from app.routers.food import router as food_router
from app.routers.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
   create_db_and_tables()
   yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(food_router)
app.include_router(meal_router)
app.include_router(profile_router)
app.include_router(auth_router)

@app.get("/")
def get_root():
   return {"message": "Willkommen zum Kalorien-Tracker API!"}