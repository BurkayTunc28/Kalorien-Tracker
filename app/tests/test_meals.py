def test_get_daily_meals(client, meal_burkay, meal_burkay_2, profile_burkay, food_poulet, food_reis):
    response = client.get(f"/meals/daily/{meal_burkay.user_id}")
    assert response.status_code == 200
    data = response.json()

    # Kalorien beider Mahlzeiten einzeln berechnen (gleiche Formel wie services/meal.py)
    kalorien_meal_1 = round((meal_burkay.menge / food_poulet.menge_gramm) * food_poulet.kalorien, 2)
    kalorien_meal_2 = round((meal_burkay_2.menge / food_reis.menge_gramm) * food_reis.kalorien, 2)

    # gesamtkalorien_heute muss die SUMME beider Mahlzeiten sein
    erwartete_gesamtkalorien = round(kalorien_meal_1 + kalorien_meal_2, 2)
    assert data["gesamtkalorien_heute"] == erwartete_gesamtkalorien

    # kalorienziel kommt aus dem Profil (BMR/GSU-Berechnung über create_profile)
    assert data["kalorienziel"] == profile_burkay.kalorienziel

    # noch_uebrig = kalorienziel - Summe aller Mahlzeiten
    assert data["noch_uebrig"] == round(profile_burkay.kalorienziel - erwartete_gesamtkalorien, 2)

    from datetime import date
    assert data["datum"] == str(date.today())

def test_delete_meal(client, meal_burkay):
    response = client.delete(f"/meals/{meal_burkay.id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}