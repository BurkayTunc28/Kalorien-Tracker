def test_login_success(client, user_burkay):
    # Korrekte Daten -> Token wird zurückgegeben
    response = client.post("/auth/login", json={
        "email": user_burkay.email,
        "password": user_burkay.password
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client, user_burkay):
    # Falsches Passwort -> 401
    response = client.post("/auth/login", json={
        "email": user_burkay.email,
        "password": "falsches_passwort"
    })
    assert response.status_code == 401


def test_get_users_without_token(client):
    # Kein Token -> 401/403, security.py greift
    response = client.get("/users/")
    assert response.status_code in (401, 403)


def test_get_users_with_token(client_burkay, user_burkay):
    # Mit gültigem Token -> 200, security.py + token_auth komplett durchlaufen
    response = client_burkay.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == user_burkay.email