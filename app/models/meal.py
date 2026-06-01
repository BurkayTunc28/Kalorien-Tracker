from sqlmodel import SQLModel, Field
from datetime import datetime, date

#Beantowrtet die Frage: "Mein Profil: Gewicht, Grösse, Alter, wie aktiv ich bin, mein Kalorienziel"
class Meal(SQLModel, table=True):
    # DB vergibt ID automatisch mit default=None
    id: int = Field(default=None, primary_key=True)

    #Angaben für das Profil eines Benutzers (ähnlich wie in einer SQL Datenbank)
    user_id: int = Field(foreign_key="user.id", index=True)
    food_id: int = Field(foreign_key="food.id", index=True)

    #Wie viel in Gram gegessen wurde
    menge: float 

    #Wie viele Kalorien die Mahlzeit enthält (berechnet aus der Menge und den Kalorien des Lebensmittels)
    kalorien: float 

    #Wann gegessen wurde (automatisch mit aktuellem Datum gefüllt)
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False
    )