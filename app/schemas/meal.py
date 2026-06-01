from datetime import datetime
#Pydantic ist eine Python-Bibliothek die Daten validiert.
# Das bedeutet: sie prüft ob die Daten den richtigen Typ haben.
from pydantic import BaseModel


class MealCreate(BaseModel):
    #optionales Feld für den Namen der Mahlzeit
    name: str | None = None
    #wer ist der User
    user_id: int
    #welches Lebensmittel aus der Datenbank
    food_id: int
    #Wie viel in Gram gegessen wurde
    menge: float

   

class MealPublic(BaseModel):
    id: int
    name: str | None
    user_id: int
    food_id: int
    menge: float
    kalorien: float
    created_at: datetime
    


  