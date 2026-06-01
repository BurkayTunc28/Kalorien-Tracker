from fastapi import APIRouter
from app.services.profile import (
    create_profile as create_profile_service,
    get_profile as get_profile_service,
    berechne_ziel as berechne_ziel_service,
    berechne_bmr,
    berechne_gsu
)
from app.schemas.profile import ProfilePublic, ProfileCreate
from app.database import SessionDep

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/")
def create_profile(profile: ProfileCreate, session: SessionDep) -> ProfilePublic:
    return create_profile_service(profile=profile, session=session)

@router.get("/{user_id}")
def get_profile(user_id: int, session: SessionDep) -> ProfilePublic:
    return get_profile_service(user_id=user_id, session=session)

@router.get("/ziel/{user_id}/{zielgewicht}")
def get_ziel(user_id: int, zielgewicht: float, session: SessionDep) -> dict:
    # 1. Profil aus DB holen
    profile = get_profile_service(user_id=user_id, session=session)
    
    # 2. BMR berechnen mit Profildaten
    bmr = berechne_bmr(
        profile.gewicht,
        profile.groesse,
        profile.alter,
        profile.geschlecht
    )
    
    # 3. GSU berechnen
    gsu = berechne_gsu(bmr, profile.aktivitaet)
    
    # 4. Ziel berechnen
    return berechne_ziel_service(
        gewicht=profile.gewicht,
        zielgewicht=zielgewicht,
        gsu=gsu
    )
