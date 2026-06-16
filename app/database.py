#Annotated → ein Python-Werkzeug um Typen mit extra Infos zu versehen (kommt später bei SessionDep)
#Depends → ein FastAPI-Werkzeug das automatisch Funktionen ausführt wenn ein Request reinkommt
#Session → ein einzelnes "Gespräch" mit der Datenbank
#SQLModel → das ORM — verbindet Python-Klassen mit Datenbanktabellen
#create_engine → erstellt die Verbindung zur Datenbank

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "kalorien_tracker.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

#Die Verbindung zur Datenbank.
#engine ist wie ein Fahrer der weiss wo die Datenbank ist.
# Er wird einmal erstellt und von allen anderen Teilen der App benutzt.
# check_same_thread: False ist nötig weil FastAPI mehrere Anfragen gleichzeitig bearbeiten kann
# Ohne das würde SQLite sich beschweren dass mehrere "Threads" gleichzeitig auf die Datei zugreifen.
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

#Erstellt alle Tabellen in der Datenbank.
#Diese Funktion wird einmal beim App-Start aufgerufen.
# Sie schaut alle deine Models an (User, Food, Meal, Profile) und erstellt daraus automatisch die Tabellen in database.db.
# Manuell SQL schreiben ist nicht nötig:
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Öffnet ein "Gespräch" mit der Datenbank.
#Jedes Mal wenn jemand einen API-Request macht (z.B. POST /foods), wird eine neue Session geöffnet.
# Die Session ist wie ein Gespräch: du sagst was du willst, die Datenbank antwortet, und wenn du
# fertig bist schliesst sich das Gespräch automatisch.
# yield bedeutet: "gib die Session raus, und wenn der Request fertig ist, räum automatisch auf."
def get_session():
    with Session(engine) as session:
        yield session

#Eine Abkürzung für die Session.
SessionDep = Annotated[Session, Depends(get_session)]