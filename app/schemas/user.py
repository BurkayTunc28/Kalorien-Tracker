from datetime import datetime
#Pydantic ist eine Python-Bibliothek die Daten validiert.
# Das bedeutet: sie prüft ob die Daten den richtigen Typ haben.
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str

class UserAuth(UserCreate):
    pass

class UserPublic(BaseModel):
    id: int
    email: str