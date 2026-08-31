# ATL 1

# Kalorien-Tracker

### ```bash ist da um den code/gewisse Abschnitte hervorzuheben

## Was macht die App?

Der Kalorien-Tracker ist dafür da, das tägliche Kalorienziel zu berechnen und zu tracken. Man gibt seine eigenen Daten ein, Grösse, Gewicht, Geschlecht, Zielgewicht und Aktivitätslevel, und das tägliche Kalorienziel wird automatisch berechnet. Für einzelne Lebensmittel wie Poulet, Reis oder Nudeln trägt man den Namen und die Nährwerte ein. Diese werden dann in Mahlzeiten zusammengefasst und vom täglichen Ziel abgezogen, damit man weiss, wo man am Tagesbedarf steht.

Die App richtet sich an Leute, die auf einfachem Weg ihren täglichen Kalorienbedarf tracken und abnehmen möchten, ohne ein kostenpflichtiges Abo abschliessen zu müssen.

Der Ursprung war ein einfaches Terminal-Script, das die Berechnungslogik (BMR/GSU nach Harris-Benedict) bereits enthielt. Von dort aus wurde die App zu einer vollständigen REST-API weiterentwickelt.



## Verwendete Technologien
- **Python 3.12**           —   Programmiersprache
- **FastAPI**               —   Web-Framework für die REST-API
- **SQLModel**              —   ORM für Datenbankzugriff zwischen Datenbank und Python
- **SQLite**                —   Lokale Datenbank
- **PyJWT**                 —   JWT-Authentifizierung
- **pytest / pytest-cov**   —   Tests und Coverage-Analyse
- **uv**                    —   Dependency-Management
- **Docker**                —   Containerisierung
- **Google Cloud Build**    —   CI/CD Pipeline

## Projektstruktur
app/

├── models/       # Datenbankmodelle — definieren wie Daten in SQLite gespeichert werden

├── schemas/      # Pydantic-Schemas — definieren was die API empfängt und zurückgibt (create & public)

├── services/     # Geschäftslogik — Berechnungen, Datenbankoperationen (Code Logik von der Terminal version)

├── routers/      # API-Endpunkte — nehmen Requests entgegen und leiten sie an Services

extras:

├── tests/        # Automatisierte Tests (pytest, 93% Coverage)

├── database.py   # Datenbankverbindung und Session-Management

├── security.py   # JWT-Authentifizierung (Token prüfen)

├── main.py       # App-Einstiegspunkt — registriert alle Router

└── terminal.py   # Ursprüngliches Terminal-Script (Ausgangsbasis der Logik)

Die Architektur folgt dem Prinzip der Schichtentrennung, jede Schicht hat genau eine Aufgabe und kommuniziert nur mit der direkt benachbarten Schicht:
Request → Router → Service → Model → Datenbank

### Übersicht aller Endpunkte in Swagger

![Swagger Übersicht - Users und Foods](docs/images/01-swagger-uebersicht-1.png)
![Swagger Übersicht - Meals, Profiles und Auth](docs/images/02-swagger-uebersicht-2.png)

Die automatisch generierte Swagger-Dokumentation zeigt alle 14 Endpunkte gruppiert nach Bereich. Das Schloss-Symbol
bei `GET /users/` zeigt an, dass dieser Endpunkt durch JWT-Authentifizierung geschützt ist.

## Installation & Starten

### Voraussetzungen
- Python 3.12
- [uv](https://docs.astral.sh/uv/) installiert

### Installation

### Repository klonen
git clone https://github.com/BurkayTunc28/Kalorien-Tracker.git

### Abhängigkeiten installieren
uv sync

### Starten
uv run fastapi dev app/main.py

Die API ist danach erreichbar unter:
- **API:** http://127.0.0.1:8000
- **Swagger UI (Dokumentation & Testen):** http://127.0.0.1:8000/docs



## Verwendung

### Typischer Ablauf

**1. User registrieren**
```bash
POST /users/
{
  "email": "beispiel@mail.ch",
  "password": "123"
}
```

![User erstellen](docs/images/03-user-erstellen.png)

Die Antwort enthält nur `id` und `email` — das Passwort wird nie zurückgegeben,
auch wenn es im Request mitgeschickt wurde.

**2. Einloggen & Token holen**
```bash
POST /auth/login
{
  "email": "beispiel@mail.ch",
  "password": "123"
}
```
![Login erfolgreich](docs/images/04-auth-erfolgreich.png)

Bei korrekten Daten wird ein `access_token` zurückgegeben (JWT). Bei falschem Passwort
kommt stattdessen ein `401 Unauthorized`:

![Login fehlgeschlagen](docs/images/05-auth-falsch.png)

Den Token kopiert man und trägt ihn oben rechts unter "Authorize" ein:

![Authorize Dialog](docs/images/06-authorize-dialog.png)

Ab jetzt sind alle geschützten Endpunkte (z.B. `GET /users/`) freigeschaltet.

**3. Lebensmittel erfassen**
```bash
POST /foods/
{
  "name": "Poulet",
  "kalorien": 120,
  "protein": 20,
  "kohlenhydrate": 30,
  "fett": 4,
  "menge_gramm": 100
}
```

![Food erstellen](docs/images/07-food-erstellen.png)

`menge_gramm` definiert auf welche Menge sich die Nährwerte beziehen, meist 100g,
kann aber auch eine andere Referenzmenge sein (z.B. 30g für eine Portion).

**4. Profil erstellen**
```bash
POST /profiles/
{
  "user_id": 1,
  "gewicht": 110,
  "groesse": 170,
  "alter": 27,
  "geschlecht": "m",
  "aktivitaet": 1,
  "zielgewicht": 90
}
```
![Profil erstellen](docs/images/08-profile-erstellen.png)

`kalorienziel` wird automatisch berechnet (BMR → GSU → -15% Defizit) und in der
Antwort zurückgegeben — der User gibt diesen Wert nirgends selbst ein. In diesem
Beispiel ergibt sich ein Kalorienziel von 2283.05 kcal/Tag.

**5. Mahlzeit erfassen**
```bash
POST /meals/
{
  "name": "Poulet Geschnetzeltes",
  "user_id": 1,
  "food_id": 1,
  "menge": 200
}
```
![Meal erstellen](docs/images/09-meal-erstellen.png)

Die Kalorien werden automatisch berechnet: `(menge / menge_gramm) * kalorien`.
Bei 200g Poulet (120 kcal/100g) ergibt das 240 kcal.

**6. Tagesübersicht abrufen**
```bash
GET /meals/daily/1
```
![Tagesübersicht](docs/images/10-daily-meals.png)

Zeigt: heute gegessene Kalorien (240), das Kalorienziel aus dem Profil (2283.05),
und wie viel noch übrig ist (2043.05). Diese Übersicht summiert automatisch alle
Mahlzeiten des aktuellen Tages.

**7. Zielgewicht-Berechnung**
```bash
GET /profiles/ziel/1
```
![Zielgewicht Berechnung](docs/images/11-profile-ziel.png)

Zeigt wie viel Gewicht noch zu verlieren ist (20 kg), das empfohlene tägliche
Defizit (403 kcal), und die geschätzte Dauer bis zum Zielgewicht (50 Wochen).


### Alle Endpunkte

- `POST /users/` — User registrieren
- `POST /auth/login` — Einloggen, Token erhalten
- `GET /users/` — Alle User abrufen (Token nötig)
- `POST /foods/` — Lebensmittel erfassen
- `GET /foods/` — Alle Lebensmittel abrufen
- `GET /foods/{id}` — Ein Lebensmittel abrufen
- `DELETE /foods/{id}` — Lebensmittel löschen
- `POST /profiles/` — Profil erstellen
- `GET /profiles/{user_id}` — Profil abrufen
- `GET /profiles/ziel/{user_id}` — Zielgewicht-Berechnung
- `POST /meals/` — Mahlzeit erfassen
- `GET /meals/user/{user_id}` — Alle Mahlzeiten eines Users
- `GET /meals/daily/{user_id}` — Tagesübersicht
- `DELETE /meals/{id}` — Mahlzeit löschen


### Was ist der Unterschied zwischen den GET-Endpunkten?

Diese Endpunkte noch konkreter erklärt:

- `GET /meals/user/{user_id}` — Alle Mahlzeiten aller Zeit (Historie)
- `GET /meals/daily/{user_id}` — Nur heutige Mahlzeiten + Vergleich mit Kalorienziel
- `GET /profiles/{user_id}` — Gespeicherte Profildaten unverändert anzeigen
- `GET /profiles/ziel/{user_id}` — NEUE Berechnung: Wochen bis Zielgewicht


## Tests

### Ausführen

Alle Tests wurden mit Intregations Testing getetestet, um die beziehungen zu einander auch wirklich zu überprüfen um nicht
einfach für eine bestimmte angabe/resultat getestet zu sein.

```bash
# Alle Tests
uv run pytest

# Mit Coverage-Bericht
uv run pytest --cov=app --cov-report=term-missing

# Einzelne Testdatei
uv run pytest app/tests/test_profiles.py -v
```

### Aktuelle Coverage: 93%

- **models/** — 100%
- **schemas/** — 100%
- **security.py** — 100%
- **routers/** — 88-100%
- **services/profile.py** — 87%
- **services/auth.py** — 91%
- **services/food.py** — 85%
- **services/meal.py** — 74%
- **services/user.py** — 77%

Services wurden hier genauer unterteilt, da die meiste Code Logik hier ist und diese dementsprechend getestet wurde.

### Was wird getestet

- **test_users.py** — User erstellen, doppelte Email, fehlendes Passwort
- **test_auth.py** — Login, falsches Passwort, JWT-Schutz
- **test_foods.py** — Lebensmittel erstellen, abrufen, löschen, 404
- **test_profiles.py** — BMR/GSU-Formel prüfen ob sie klappt, Zielgewicht-Berechnung
- **test_meals.py** — Kalorienberechnung, Tagessumme, löschen

## Überlegungen während der Entwicklung

## Warum überhaupt die Kalorietracker App?
Es war eine eigene Frustation, da ich privat intensiver auf meine Ernährung achten wollte, musste ich das aktiv
dokumentieren. Es gibt dafür zwar zahlreiche Apps, aber jedes von ihnen arbeitet mit einem Abo model, welches
Pflicht wird nach 1-2 Wochen. Da ich im Studium den Fokus auf Softwareentwicklung habe, beschloss ich deswegen
meine eigene Version der App zu erstellen.

### Von Terminal zu API
Der Ausgangspunkt war eine einfache Terminal Version (`terminal.py`) das Gewicht, Grösse, Alter und Aktivitätslevel
per `input()` abfragt und daraus den Kalorienbedarf berechnet. Das Ziel war, diese Logik in eine echte REST-API zu
überführen, ohne die Berechnungsformeln zu verändern, nur die Ein- und Ausgabe zu ersetzen: statt `input()` kommen
die Daten jetzt aus dem HTTP-Request-Body, statt `print()` gibt es eine JSON-Response.

### Schichtentrennung (models/schemas/services/routers)
Von Beginn an war klar, dass der Code sauber getrennt sein soll. Jede Schicht hat genau eine Aufgabe:
-Models definieren die Datenbankstruktur
-Schemas validieren was rein- und rausgeht,
-Services enthalten die Logik,
-Routers nehmen Requests über HTTP entgegen.
Das macht den Code nachvollziehbar und erweiterbar, eine neue Funktion
kann hinzugefügt werden ohne bestehende Schichten anzufassen und der Code ist dementsprechend auch lesbarer/nachvollziehbarer.

### Kalorienberechnung über Referenzmenge
Lebensmittel haben unterschiedliche Referenzmengen, Poulet wird typischerweise pro 100g angegeben,
ein Müsliriegel pro Portion (z.B. 30g). Deshalb wurde das Feld `menge_gramm` eingeführt, das flexibel
definiert werden kann. Die Berechnung `(menge / menge_gramm) * kalorien` funktioniert für beide Fälle korrekt
für die Meal berechnung.

### Kalorienziel automatisch berechnet
Das Kalorienziel wird nicht manuell eingegeben, sondern beim Erstellen des Profils automatisch
berechnet: BMR (Grundumsatz nach Harris-Benedict) × PAL-Faktor (Aktivitätslevel) = GSU (Gesamtumsatz),
davon 15% Defizit = tägliches Kalorienziel. Das ist medizinisch fundiert und verhindert ein zu grosses
Kaloriendefizit und erlaubt ein gesundes Abnehmen.

### JWT-Authentifizierung
Damit nicht jeder auf alle Daten zugreifen kann, wurde JWT (JSON Web Token) eingebaut. Nach dem Login erhält
der User einen Token der bei geschützten Endpunkten mitgeschickt wird. Der Server prüft den Token und weiss
damit wer der User ist, ohne jedes Mal das Passwort zu übertragen.


## Was ich noch verbessern würde

### Mehrere Lebensmittel pro Mahlzeit
Aktuell besteht eine Mahlzeit immer aus genau einem Lebensmittel. Ein realistisches Gericht wie
"Poulet mit Reis und Salat" müsste als drei separate Mahlzeiten eingetragen werden.
Mit mehr Zeit und Verständniss für die Komplexität hätte ich eine "MealItem"-Zwischentabelle eingeführt:

Meal (Name, Datum, User)
─ MealItem 1: Poulet, 200g
─ MealItem 2: Reis, 100g
─ MealItem 3: Salat, 50g

Die Kalorienberechnung würde dann die Summe aller Items ergeben.

### Food Datenbank
Eventuell eine Verkpüfung mit einer Datenbank, die allgemeine Infos zu Lebensmittel hätten, damit man die
Kalorien, Proteine, Kohlenhydrate nicht immer separat eingeben muss, wenn man es in der Datenbank finden kann.

### Monatsübersicht
Aktuell gibt es nur eine Tagesübersicht. Eine Monatsübersicht wäre technisch einfach umzusetzen
(gleiche Logik wie `get_daily_meals`, nur mit Monatsfilter statt Tagesfilter) und würde einen
besseren Überblick über längere Zeiträume geben.

### Benutzeroberfläche
Die App ist aktuell nur über die Swagger UI oder direkt per API nutzbar. Ein einfaches Web-Frontend
(z.B. mit React oder einer mobilen App) würde die Nutzung deutlich komfortabler machen.

# ATL 2

## Ausgangslage

Das Softwareprojekt aus ATL 1 lief bisher nur lokal auf meinem Laptop. Ziel von ATL 2 war es, die App
in der Google Cloud verfügbar zu machen, mit einer automatisierten Pipeline, die bei jedem Push die Tests
ausführt und nur bei erfolgreichen Tests ein Deployment durchführt. Damit die Software von mehreren Benutzern
gleichzeitig genutzt werden kann, sollte sie in der Cloud gehostet und im Internet verfügbar sein.

## Auftrag

Konkret ging es darum:

- Google Cloud Projekt einrichten (inkl. Budget-Alarm)
- Cloud Build mit dem GitHub-Repository verbinden und einen Trigger einrichten
- Bei jedem Push: Tests automatisch ausführen
- Bei erfolgreichen Tests: Docker-Image bauen und in die Artifact Registry hochladen
- Das Image als Cloud Run Service deployen
- Nachweisen, dass die Pipeline bei einem fehlschlagenden Test korrekt abbricht
- Nachweisen, dass die Pipeline korrekt funktioniert bis zum Deploy

Die Einrichtung von Cloud Build, Artifact Registry und Cloud Run wurde gemeinsam mit dem Dozenten im Unterricht
anhand einer Live-Demonstration erarbeitet, basierend auf den bereitgestellten Aufgabenblättern (Woche 16/17).
Daher waren die Herausforderungen in diesem Teil nicht allzu gross. Es gab natürlich noch Probleme im eigenen
Rahmen, welche zwar nicht direkt in der ATL2 verlangt waren, aber die ich dennoch lösen wollte:

Die Umstellung von SQLite auf Postgres, wofür ich einen separaten Eintrag gegen Ende dieser Dokumentation erstellt habe.

## Google Cloud Projekt & Budget

Für das Projekt wurde ein Google Cloud Account mit dem Projekt `HE24-PE A-Burkay` eingerichtet. Um sicherzustellen,
dass keine unerwarteten Kosten entstehen, habe ich zusätzlich ein Budget mit Alarm-Schwellen bei 50%, 90% und 100%
von CHF 5.- eingerichtet:

![Budget-Einrichtung](docs/ATL-2-Bilder/Budget.png)

## Die Pipeline (cloudbuild.yaml)

Damit die App überhaupt automatisch getestet und deployed werden kann, musste Cloud Build zuerst wissen, wo sich
mein Code befindet und wann es aktiv werden soll. Das Ergebnis ist eine Pipeline, die komplett ohne manuelles
Eingreifen bei jedem Push abläuft, vom Testen bis zum fertigen, live erreichbaren Service.

### GitHub-Verknüpfung

Damit Cloud Build bei jedem Push automatisch reagieren kann, wurde das GitHub-Repository über die
offizielle "Google Cloud Build"-GitHub-App mit Cloud Build verbunden. Diese App ist unter den
installierten GitHub Apps des Repositories sichtbar:

![Google Cloud Build als installierte GitHub App](docs/ATL-2-Bilder/Verknuepfung-GitHub-Cloud-Run-4.png)

In Cloud Build selbst ist ein Trigger `HE24-Blog-Burkay` eingerichtet, der auf das Repository
`BurkayTunc28/Kalorien-Tracker` hört:

![Cloud Build Trigger-Übersicht](docs/ATL-2-Bilder/Verknuepfung-GitHub-Cloud-Run.png)

Der Trigger reagiert auf das Event "Push to a branch" und ist mit dem Repository verknüpft:

![Trigger-Konfiguration: Quelle und Event](docs/ATL-2-Bilder/Verknuepfung-GitHub-Cloud-Run-2.png)

Konkret wird der Trigger nur bei Pushes auf den `main`-Branch ausgelöst (`^main$` als Regex), und
verwendet die `cloudbuild.yaml` im Repository-Root als Build-Konfiguration:

![Trigger-Konfiguration: Branch und Build-Datei](docs/ATL-2-Bilder/Verknuepfung-GitHub-Cloud-Run-3.png)

### Die vier Schritte

Die komplette Pipeline besteht aus vier Schritten, die strikt nacheinander ausgeführt werden. Jeder Schritt läuft
nur, wenn der vorherige erfolgreich war:

1. **Run Tests** — Nimmt das offizielle Python 3.12 Image als Container für diesen Schritt, installiert die Abhängigkeiten via `uv` und führt `pytest app/tests/ -v` aus
2. **Build Container Image** — baut das Docker-Image mit `docker build` aus dem Dockerfile
3. **Push Container Image to Registry** — lädt das eben gebaute Image in die Google Artifact Registry hoch
4. **Deploy to Cloud Run** — deployt das Image als Cloud Run Service

Eine Anmerkung zu den Tests: Ich habe nirgends manuell festgelegt, welche Tests laufen sollen. `pytest` durchsucht automatisch
den Ordner `app/tests/` nach allen Dateien und Funktionen, die mit `test_` beginnen (Test-Discovery). Jeder neue
Test, den ich hinzufüge, wird beim nächsten Push automatisch mitgetestet, ohne dass ich die Pipeline anpassen muss.

Da die Schritte sequenziell voneinander abhängen, genügt ein einziger fehlgeschlagener Test, damit Cloud Build die gesamte Pipeline abbricht.
Build, Push und Deploy werden dann gar nicht erst ausgeführt. Das wird auch getestet und mit Bildern nachgewiesen.

Die vollständige Konfiguration ist in cloudbuild.yaml im Repository-Root einsehbar, wo auch alles mit genaueren Kommentaren ausgestattet wurde.

### Dockerfile

Damit der "Build Container Image"-Schritt ein möglichst schlankes und produktionstaugliches Image erzeugt,
verwendet das Dockerfile einen Multi-Stage-Build:

```dockerfile
FROM python:3.12-alpine AS builder
WORKDIR /app
RUN pip install uv
COPY uv.lock pyproject.toml ./
RUN uv export --no-dev --format requirements.txt --no-hashes --no-header --no-annotate > requirements.txt

FROM python:3.12-alpine
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /root/.cache
RUN rm -rf /tmp/*
RUN rm -rf /app/requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY ./app ./
EXPOSE 8100
ENTRYPOINT ["fastapi", "run", "main.py"]
CMD ["--port", "8100"]
```

In der ersten Stage (`builder`) wird `uv` nur genutzt, um aus `pyproject.toml`/`uv.lock` eine
`requirements.txt` mit den reinen Produktions-Abhängigkeiten zu erzeugen (`--no-dev` schliesst
Test-Werkzeuge wie `pytest-cov` aus). Die zweite Stage installiert nur diese `requirements.txt` und
verwirft danach alle Build-Werkzeuge sowie Caches wieder, im finalen Image landet also nur das, was
zur Laufzeit tatsächlich gebraucht wird. Zusammen mit der schlanken `alpine`-Basis ergibt das ein Image
von rund 50 MB (sichtbar in der Artifact Registry weiter unten), was schnellere Uploads und schnellere
Cloud Run Startzeiten ermöglicht.

Der `EXPOSE 8100` und `CMD ["--port", "8100"]` sind bewusst auf denselben Port abgestimmt, den auch die
`cloudbuild.yaml` beim Cloud Run Deployment erwartet (`--port=8100`), nur wenn beide übereinstimmen,
kann Cloud Run erkennen, dass der Container erfolgreich gestartet ist und auf Anfragen wartet.

### Artifact Registry

Damit das gebaute Docker-Image nicht bei jedem Deployment neu gebaut werden muss und nachvollziehbar bleibt,
welche Version wann gebaut wurde, lädt die Pipeline jedes Image in die Google Artifact Registry hoch. Das
Ergebnis ist eine vollständige, versionierte Historie aller bisherigen Builds, auf die Cloud Run beim
Deployment direkt zugreifen kann.

Das gebaute Image wird bei jedem Push mit einem eindeutigen Tag (`$COMMIT_SHA`) in der Artifact Registry abgelegt.
So ist jedes Image eindeutig einem Git-Commit zugeordnet, und die komplette Historie aller bisherigen Builds bleibt
nachvollziehbar:

![Artifact Registry Repository-Übersicht](docs/ATL-2-Bilder/Artifact-Registry.png)
![Artifact Registry Package-Ansicht](docs/ATL-2-Bilder/Artifact-Registry-2.png)
![Artifact Registry Image-Liste mit allen Versionen](docs/ATL-2-Bilder/Artifact-Registry-3.png)

### Cloud Run

Der letzte Schritt der Pipeline deployt das fertige Image als Cloud Run Service — das ist der Teil, der
das Projekt tatsächlich von "läuft nur lokal" zu "ist im Internet erreichbar" macht. Cloud Run wurde
gewählt, weil es serverlos ist: Es skaliert bei fehlender Nutzung automatisch auf 0 Instanzen herunter
und verursacht dann keine Kosten, im Gegensatz zu einem dauerhaft laufenden Server.

Nach erfolgreichem Deployment ist die App öffentlich unter folgender URL erreichbar:

`https://kalorien-tracker-1082755787497.europe-west6.run.app` und/oder `https://kalorien-tracker-1082755787497.europe-west6.run.app/docs`

![Cloud Run Übersicht](docs/ATL-2-Bilder/Cloud-Run.png)
![Cloud Run Service Details](docs/ATL-2-Bilder/Cloud-Run-2.png)

Die API läuft live und antwortet korrekt:

![Cloud Run live erreichbar - Root Endpoint](docs/ATL-2-Bilder/Cloud-Run-3.png)
![Cloud Run live erreichbar - Swagger UI](docs/ATL-2-Bilder/Cloud-Run-4.png)

## Nachweis: Cloud Build bricht bei fehlschlagendem Test ab

Um zu überprüfen, dass die Pipeline korrekt reagiert, wenn ein Test fehlschlägt, habe ich die Erwartung
in `test_create_user` (`app/tests/test_users.py`) verändert.

**Ursprünglicher, korrekter Test:**

![Test korrekt](docs/ATL-2-Bilder/Create-User-Test-Korrekte-Version.png)

**Bewusst veränderter Test** — der erwartete Status-Code wurde von 200 auf 201 gesetzt, obwohl der Endpoint
tatsächlich 200 zurückgibt:

![Test bewusst fehlerhaft](docs/ATL-2-Bilder/Create-User-Test-Falsche-Version.png)

Nach dem Push zeigt sich: Cloud Build erkennt den fehlgeschlagenen Test (`assert 200 == 201`) und bricht die
Pipeline direkt nach Schritt "Run Tests" ab. Die nachfolgenden Schritte (Build, Push, Deploy) werden nicht mehr
ausgeführt, es wird also nichts Fehlerhaftes deployed:

![Build fehlgeschlagen](docs/ATL-2-Bilder/Cloud-Build-Fehlermeldung-201-statt-200-bei-Assert.png)

Nachdem ich die Änderung rückgängig gemacht und erneut gepusht habe, läuft die Pipeline wieder vollständig durch,
inklusive des zuvor fehlgeschlagenen Tests, der nun wieder grün ist:

![Build wieder erfolgreich](docs/ATL-2-Bilder/Cloud-Build-Korrekte-Version.png)

## Herausforderungen während der Entwicklung

### Postgres in der Cloud vs. lokale Entwicklung

Im Rahmen einer separaten Übung habe ich mein Projekt lokal auf PostgreSQL via **Docker Compose** umgestellt
(`docker-compose.yaml` mit `db`- und `pgadmin`-Service). Diese Änderung wurde zunächst versehentlich auch in
den `main`-Branch gepusht, der von der Cloud Build Pipeline verwendet wird.

Das führte zu zwei aufeinanderfolgenden Fehlern:

1. **Tests schlugen fehl:** `conftest.py` versuchte sich mit einer Postgres-Datenbank auf `localhost:5432` zu
   verbinden. Der "Run Tests"-Schritt in Cloud Build ist aber ein einfacher `python:3.12`-Container ohne
   laufenden Datenbankserver — die Verbindung schlug mit `Connection refused` fehl.

![Cloud Build Fehler-Übersicht: alle Tests scheitern](docs/ATL-2-Bilder/Fehler-Postgres.png)
![Detaillierter Fehler: psycopg2 Connection refused](docs/ATL-2-Bilder/Fehler-Postgres-2.png)

2. **Nachdem die Tests korrigiert waren, schlug das Deployment fehl:** `app/database.py` hatte dieselbe
   Umstellung erhalten. Beim App-Start versuchte `create_db_and_tables()` sich ebenfalls mit Postgres zu
   verbinden, die App stürzte deshalb sofort ab (`Container called exit(3)`), bevor sie überhaupt anfangen
   konnte, auf dem erwarteten Port zu lauschen. Cloud Run meldete: *"The user-provided container failed to
   start and listen on the port..."*

### Überlegung zu einer Postgres-Lösung in der Cloud

Ich habe mich gefragt, ob ich statt SQLite auch
in der Cloud durchgehend Postgres nutzen könnte. Dabei bin ich auf ein technisches und finanzielles Problem
gestossen: Cloud Run selbst kann keinen Datenbankserver "mitlaufen lassen", es deployt ausschliesslich einzelne,
zustandslose Container. Eine dauerhaft erreichbare Postgres-Instanz in der Google Cloud wäre nur über Cloud SQL
möglich, einen separaten, verwalteten Datenbank-Service. Cloud SQL läuft aber rund um die Uhr und verursacht
laufende Kosten (auch bei der kleinsten Konfiguration mehrere Franken pro Monat) — im Gegensatz zu Cloud Run,
das bei fehlender Nutzung auf 0 Instanzen herunterskaliert und dann nichts kostet. Da ich kein Google-Cloud-
Startguthaben mehr zur Verfügung hatte, hätte das mein eingerichtetes Budget (CHF 5.-) direkt überschritten.

**Lösung:** Ich habe die Datenbank-Verbindung in `database.py` und `conftest.py` so umgebaut, dass sie über eine
Umgebungsvariable gesteuert wird, mit Postgres als Standardwert (Fallback):

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://kalorientracker:kalorientracker@localhost:5432/kalorientracker"
)
```

- **Lokal auf meinem Rechner:** Die Variable ist nicht gesetzt, daher greift der Postgres-Fallback, die App
  verbindet sich mit meiner lokalen Docker-Compose-Postgres-Datenbank.

- **In Cloud Build und Cloud Run:** Die Variable wird in `cloudbuild.yaml` explizit auf SQLite gesetzt
  (`--set-env-vars=DATABASE_URL=sqlite:///kalorien_tracker.db` beim Deployment, bzw.
  `export TEST_DATABASE_URL="sqlite:///database_test.db"` vor den Tests) und überschreibt damit den Fallback.

So läuft dieselbe Codebasis lokal mit Postgres (erfüllt die separate Docker-Übung) und in der Cloud kostenlos
mit SQLite (erfüllt ATL 2), ohne dass eine kostenpflichtige Cloud-SQL-Instanz nötig ist. Eine Lösung, bei der
dieselbe Postgres-Instanz für beide Umgebungen genutzt wird, ohne laufende Kosten zu verursachen, konnte ich
nicht finden, das wäre ein möglicher nächster Schritt (z.B. mit einem befristeten Google-Cloud-Testguthaben).

Die genaue Umsetzung ist in [`app/database.py`](app/database.py), [`app/tests/conftest.py`](app/tests/conftest.py)
und [`cloudbuild.yaml`](cloudbuild.yaml) nachvollziehbar. Die lokale Postgres-Umgebung selbst ist in
[`docker-compose.yaml`](docker-compose.yaml) definiert (Postgres- und PgAdmin-Service).

Diese Situation hat mir gezeigt, wie wichtig es ist, Umgebungsvariablen mit sinnvollen Fallback-Werten sauber
von der eigentlichen Produktionskonfiguration zu trennen, und wie aufschlussreich Cloud Build/Cloud Run Logs
beim Debugging von Deployment-Problemen sind.

## Fazit

Mit ATL 2 ist der Kalorien-Tracker vom reinen Lokal-Projekt zu einer Anwendung geworden, die automatisch
getestet, gebaut und in die Cloud deployed wird, bei jedem Push, ohne manuellen Eingriff. Es hat mir gezeigt, wie
so ein automatisierter Ablauf in einer realen Umgebung ungefähr aussehen würde, und es hatte einen deutlichen Lerneffekt für mich,
nicht nur für das Studium oder für die Arbeit, sondern auch für meine zukünftigen privaten Projekte.

Ein wichtiger Punkt, den ich mitnehmen konnte: Das Debugging der Postgres/SQLite-Problematik hat mir gezeigt, wie wichtig eine
saubere Trennung von Umgebungen (lokal vs. Cloud) ist, und die Auseinandersetzung mit den Kosten von Cloud SQL hat mir ein
besseres Gefühl dafür gegeben, wie schnell in der Cloud laufende Kosten entstehen können, wenn man Cloud Run nicht mit
Vorsicht aufsetzt.

Insgesamt war ATL 2 eine gute praktische Ergänzung zu ATL 1, in der ich viele Aspekte kennenlernen durfte für meinen
Werdegang als Softwareentwickler.