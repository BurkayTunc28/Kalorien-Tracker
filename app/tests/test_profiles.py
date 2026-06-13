def test_create_profile(client, profile_burkay_daten, erwartetes_kalorienziel):
    response = client.post("/profiles/", json=profile_burkay_daten)
    assert response.status_code == 200
    data = response.json()

    # kalorienziel muss der Formel BMR -> GSU -> -15% entsprechen
    assert data["kalorienziel"] == erwartetes_kalorienziel


def test_get_ziel(client, profile_burkay):
    response = client.get(f"/profiles/ziel/{profile_burkay.user_id}")
    assert response.status_code == 200
    data = response.json()

    # "zu_verlieren" muss der Differenz aus dem Profil entsprechen,
    # unabhängig von den konkreten Werten in profile_burkay
    erwartete_differenz = round(profile_burkay.gewicht - profile_burkay.zielgewicht, 2)
    assert data["zu_verlieren"] == erwartete_differenz

    # dauer_wochen muss vorhanden und plausibel (positiv) sein
    assert "dauer_wochen" in data
    assert data["dauer_wochen"] > 0