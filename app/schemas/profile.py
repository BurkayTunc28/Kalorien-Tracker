from datetime import datetime
#Pydantic ist eine Python-Bibliothek die Daten validiert.
# Das bedeutet: sie prüft ob die Daten den richtigen Typ haben.
from pydantic import BaseModel


class ProfileCreate(BaseModel):
    #optionales Feld für den Namen der Mahlzeit
    user_id: int
    gewicht: float
    groesse: float
    alter: int
    geschlecht: str
    aktivitaet: int
    
   
class ProfilePublic(BaseModel):
    id: int
    user_id: int
    gewicht: float
    groesse: float
    alter: int
    geschlecht: str
    aktivitaet: int
    kalorienziel: float
    created_at: datetime
    