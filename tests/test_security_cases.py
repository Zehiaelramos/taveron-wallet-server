import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_unauthorized_access_to_other_user_data(client: AsyncClient):
    """Verifica que un usuario no pueda ver datos de otro usuario (IDOR Protection)."""
    
    # 1. Crear Usuario A y su tarjeta
    await client.post("/auth/register", json={"email": "userA@test.com", "password": "password123"})
    login_A = await client.post("/auth/login", data={"username": "userA@test.com", "password": "password123"})
    token_A = login_A.json()["access_token"]
    
    res_A = await client.post("/payment-methods/", 
        json={"type": "card", "alias": "Card A", "institution": "Bank A", "identifier": "1111222233334444"},
        headers={"Authorization": f"Bearer {token_A}"}
    )
    pm_id_A = res_A.json()["id"]

    # 2. Crear Usuario B
    await client.post("/auth/register", json={"email": "userB@test.com", "password": "password123"})
    login_B = await client.post("/auth/login", data={"username": "userB@test.com", "password": "password123"})
    token_B = login_B.json()["access_token"]

    # 3. Usuario B intenta ver la tarjeta del Usuario A: Debe dar 404 (o 403)
    response = await client.get(f"/payment-methods/{pm_id_A}", headers={"Authorization": f"Bearer {token_B}"})
    assert response.status_code == 404  # El repo filtra por user_id, así que simplemente no lo encuentra

@pytest.mark.asyncio
async def test_invalid_token_access(client: AsyncClient):
    """Verifica que el acceso sea denegado con un token inválido."""
    response = await client.get("/payment-methods/", headers={"Authorization": "Bearer token-falso-123"})
    assert response.status_code == 401
    assert "No se pudo validar las credenciales" in response.json()["detail"]

@pytest.mark.asyncio
async def test_pagination_out_of_bounds(client: AsyncClient):
    """Verifica comportamiento con paginación fuera de límites."""
    # Login
    await client.post("/auth/register", json={"email": "page_edge@test.com", "password": "password123"})
    login = await client.post("/auth/login", data={"username": "page_edge@test.com", "password": "password123"})
    token = login.json()["access_token"]
    
    # Pedir con skip muy alto
    response = await client.get("/payment-methods/?skip=1000", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 0
