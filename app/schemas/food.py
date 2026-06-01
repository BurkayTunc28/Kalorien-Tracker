from datetime import datetime
#Pydantic ist eine Python-Bibliothek die Daten validiert.
# Das bedeutet: sie prüft ob die Daten den richtigen Typ haben.
from pydantic import BaseModel


class FoodCreate(BaseModel):
    name: str
    kalorien: float
    protein: float
    kohlenhydrate: float
    fett: float

class FoodPublic(BaseModel):
    id: int
    created_at: datetime
    name: str
    kalorien: float
    protein: float
    kohlenhydrate: float
    fett: float