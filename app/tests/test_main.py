from app.services.profile import berechne_bmr

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_berechne_bmr_mann():
    result = berechne_bmr(gewicht=80, groesse=180, alter=25, geschlecht="m")
    assert round(result, 1) == 1891.8