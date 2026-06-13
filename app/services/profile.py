import math
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate
from app.database import SessionDep
from sqlmodel import select
from fastapi import HTTPException

def berechne_bmr(gewicht: float, groesse: float, alter: int, geschlecht: str) -> float:
    if geschlecht == "m":
        bmr = 66.5 + (13.67 * gewicht) + (5.003 * groesse) - (6.755 * alter)
    
    elif geschlecht == "w":
        bmr = 655 + (9.563 * gewicht) + (1.850 * groesse) - (4.676 * alter)

    else:
        raise HTTPException(status_code=400, detail="Geschlecht muss 'm' oder 'w' sein")

    return bmr

# PAL-Faktoren als Dictionary statt if/elif
PAL_FAKTOREN = {
    1: 1.2,    # Sitzend
    2: 1.375,  # Leicht aktiv
    3: 1.55,   # Moderat aktiv
    4: 1.725,  # Sehr aktiv
    5: 1.9     # Extrem aktiv
}

def berechne_gsu(bmr: float, aktivitaet: int) -> float:
    #Berechnet den Gesamtumsatz (GSU = BMR × PAL-Faktor)
    if aktivitaet not in PAL_FAKTOREN:
        raise HTTPException(status_code=400, detail="Aktivitätslevel muss zwischen 1 und 5 sein")
    
    pal_faktor = PAL_FAKTOREN[aktivitaet]

    return bmr * pal_faktor

def create_profile(profile: ProfileCreate, session: SessionDep) -> Profile:
    # 1. BMR berechnen
    bmr = berechne_bmr(profile.gewicht, profile.groesse, profile.alter, profile.geschlecht)
    
    # 2. GSU berechnen
    gsu = berechne_gsu(bmr, profile.aktivitaet)
    
    # 3. Kalorienziel berechnen (GSU - 15% Defizit)
    kalorienziel = gsu - (gsu * 0.15)
    
    # 4. Profil-Objekt erstellen mit berechnetem Kalorienziel
    db_profile = Profile(
        user_id=profile.user_id,
        gewicht=profile.gewicht,
        groesse=profile.groesse,
        alter=profile.alter,
        geschlecht=profile.geschlecht,
        aktivitaet=profile.aktivitaet,
        zielgewicht=profile.zielgewicht,
        kalorienziel=round(kalorienziel, 2)
    )
    
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile

def get_profile(user_id: int, session: SessionDep) -> Profile:
    profile = session.exec(select(Profile).where(Profile.user_id == user_id)).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profil nicht gefunden")
    return profile

def berechne_ziel(gewicht: float, zielgewicht: float, gsu: float) -> dict:
    #Berechnet Dauer und wöchentlichen Verlust bis zum Zielgewicht
    defizit_pro_tag = gsu * 0.15
    verlust_pro_woche = (defizit_pro_tag * 7) / 7000
    zu_verlieren = gewicht - zielgewicht
    dauer = zu_verlieren / verlust_pro_woche
    
    return {
        "zu_verlieren": round(zu_verlieren, 2),
        "defizit_pro_tag": round(defizit_pro_tag),
        "kalorienziel": round(gsu - defizit_pro_tag),
        "verlust_pro_woche": round(verlust_pro_woche, 2),
        "dauer_wochen": math.ceil(dauer)
    }