#startet die App und kriegt man die korrekte begrüssung
def test_read_root_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Willkommen zum Kalorien-Tracker API!"}

def test_create_user(client):
    response = client.post("/users", json={"email": "burkay@test.ch", "password": "1234"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "password" not in data

def test_unique_email(client, user_burkay):
    response = client.post("/users/", json={
        "email": "burkay@test.ch",
        "password": "1234",
    })
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "Email already exists."

def test_no_password(client):
    response = client.post("/users/", json={
        "email": "burkay@test.ch"
    })
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "Field required"
    assert "password" in data["detail"][0]["loc"]