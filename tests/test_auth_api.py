import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Prueba el flujo de registro exitoso."""
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "strongpassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Prueba que no se permitan emails duplicados."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "full_name": "User 1"
    }
    # Primer registro
    await client.post("/auth/register", json=user_data)
    
    # Segundo registro (mismo email)
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "El correo electrónico ya está registrado."

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Prueba el inicio de sesión exitoso."""
    # 1. Registrar usuario
    await client.post(
        "/auth/register",
        json={"email": "login@test.com", "password": "password123"}
    )
    
    # 2. Login (Usando OAuth2 Form)
    response = await client.post(
        "/auth/login",
        data={"username": "login@test.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient):
    """Prueba el cierre de sesión exitoso."""
    # Login previo
    await client.post("/auth/register", json={"email": "logout@test.com", "password": "password123"})
    login_res = await client.post("/auth/login", data={"username": "logout@test.com", "password": "password123"})
    token = login_res.json()["access_token"]
    
    # Logout
    response = await client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "Sesión cerrada" in response.json()["message"]

@pytest.mark.asyncio
async def test_login_failed(client: AsyncClient):
    """Prueba que un login fallido devuelva 401."""
    response = await client.post(
        "/auth/login",
        data={"username": "nonexistent@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas."
