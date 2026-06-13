from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

#Beantowrtet die Frage: "Lebensmittel: Name, Kalorien, Protein, Kohlenhydrate, Fett"
class Food(SQLModel, table=True):
    # DB vergibt ID automatisch mit default=None
    id: int = Field(default=None, primary_key=True)

    #Angaben für die Nährwerte eines Lebensmittels (ähnlich wie in einer SQL Datenbank)
    name: str = Field(index=True)
    kalorien: float
    protein: float
    kohlenhydrate: float
    fett: float
    menge_gramm: float

    #Wann das Lebensmittel Eintrag erstellt wurde (automatisch mit aktuellem Datum gefüllt)
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False
    )

    