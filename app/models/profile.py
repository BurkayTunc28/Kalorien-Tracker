from sqlmodel import SQLModel, Field
from datetime import datetime

#Beantowrtet die Frage: "Mein Profil: Gewicht, Grösse, Alter, wie aktiv ich bin, mein Kalorienziel"
class Profile(SQLModel, table=True):
    # DB vergibt ID automatisch mit default=None
    id: int = Field(default=None, primary_key=True)

    #Angaben für das Profil eines Benutzers (ähnlich wie in einer SQL Datenbank)
    gewicht: float
    groesse: float
    alter: int
    geschlecht: str
    aktivitaet: int
    kalorienziel: float
    user_id: int = Field(foreign_key="user.id", index=True)
   

    #Wann das der Profileintrag erstellt wurde (automatisch mit aktuellem Datum gefüllt)
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False
    )