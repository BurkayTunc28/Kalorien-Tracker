def test_food_with_custom_menge_gramm(client):
    response = client.post("/foods/", json={
        "name": "Müsliriegel",
        "menge_gramm": 30,
        "kalorien": 120,
        "protein": 3,
        "kohlenhydrate": 18,
        "fett": 4
    })
    assert response.status_code == 200
    data = response.json()
    assert data["menge_gramm"] == 30

def test_get_food_not_found(client):
    # Nicht existierende ID -> 404
    response = client.get("/foods/999")
    assert response.status_code == 404

def test_delete_food(client, food_poulet):
    # DELETE -> ok, danach 404
    response = client.delete(f"/foods/{food_poulet.id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    response = client.get(f"/foods/{food_poulet.id}")
    assert response.status_code == 404