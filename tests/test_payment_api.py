import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_full_payment_method_cycle(client: AsyncClient):
    """Prueba el ciclo completo: Registro -> Login -> Crear PM -> Listar -> Ver Detalle."""
    
    # 1. Registrar e Iniciar Sesión
    user_data = {"email": "wallet@test.com", "password": "password123"}
    await client.post("/auth/register", json=user_data)
    login_res = await client.post("/auth/login", data={"username": user_data["email"], "password": user_data["password"]})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Crear un método de pago
    pm_data = {
        "type": "card",
        "alias": "Tarjeta de Débito",
        "institution": "Banorte",
        "currency": "MXN",
        "identifier": "4111222233334444"
    }
    create_res = await client.post("/payment-methods/", json=pm_data, headers=headers)
    assert create_res.status_code == 201
    pm_id = create_res.json()["id"]
    assert create_res.json()["masked_identifier"] == "**** 4444"

    # 3. Listar métodos (Verificar enmascaramiento)
    list_res = await client.get("/payment-methods/", headers=headers)
    assert len(list_res.json()) == 1
    assert list_res.json()[0]["masked_identifier"] == "**** 4444"

    # 4. Ver Detalle (Verificar dato completo descifrado)
    detail_res = await client.get(f"/payment-methods/{pm_id}", headers=headers)
    assert detail_res.status_code == 200
    assert detail_res.json()["full_identifier"] == "4111222233334444"

@pytest.mark.asyncio
async def test_filtering_payment_methods(client: AsyncClient):
    """Verifica que el filtrado por tipo funcione."""
    user_data = {"email": "filter@test.com", "password": "password123"}
    await client.post("/auth/register", json=user_data)
    login_res = await client.post("/auth/login", data={"username": user_data["email"], "password": user_data["password"]})
    headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    # Crear una Tarjeta
    await client.post("/payment-methods/", json={
        "type": "card", "alias": "T1", "institution": "X", "identifier": "1234567890123456"
    }, headers=headers)
    # Crear una CLABE
    await client.post("/payment-methods/", json={
        "type": "clabe", "alias": "C1", "institution": "Y", "identifier": "123456789012345678"
    }, headers=headers)

    # Filtrar por 'card'
    res = await client.get("/payment-methods/?type=card", headers=headers)
    assert len(res.json()) == 1
    assert res.json()[0]["type"] == "card"

@pytest.mark.asyncio
async def test_update_payment_method_status(client: AsyncClient):
    """Verifica el cambio de estatus (ACTIVE/INACTIVE)."""
    user_data = {"email": "status@test.com", "password": "password123"}
    await client.post("/auth/register", json=user_data)
    login_res = await client.post("/auth/login", data={"username": user_data["email"], "password": user_data["password"]})
    headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    pm = await client.post("/payment-methods/", json={
        "type": "card", "alias": "Status Test", "institution": "X", "identifier": "1234567890123456"
    }, headers=headers)
    pm_id = pm.json()["id"]

    # Cambiar a INACTIVE
    patch_res = await client.patch(f"/payment-methods/{pm_id}/status?status=inactive", headers=headers)
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "inactive"

@pytest.mark.asyncio
async def test_duplicate_payment_method(client: AsyncClient):
    """Verifica que no se permita registrar la misma tarjeta dos veces."""
    user_data = {"email": "dup@test.com", "password": "password123"}
    await client.post("/auth/register", json=user_data)
    login_res = await client.post("/auth/login", data={"username": user_data["email"], "password": user_data["password"]})
    headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    pm_data = {"type": "card", "alias": "T1", "institution": "X", "identifier": "1234567890123456"}
    await client.post("/payment-methods/", json=pm_data, headers=headers)
    response = await client.post("/payment-methods/", json=pm_data, headers=headers)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_soft_delete_payment_method(client: AsyncClient):
    """Verifica que el borrado sea lógico."""
    user_data = {"email": "delete@test.com", "password": "password123"}
    await client.post("/auth/register", json=user_data)
    login_res = await client.post("/auth/login", data={"username": user_data["email"], "password": user_data["password"]})
    headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    pm = await client.post("/payment-methods/", json={
        "type": "card", "alias": "Borrar", "institution": "X", "identifier": "1234567890123456"
    }, headers=headers)
    pm_id = pm.json()["id"]

    await client.delete(f"/payment-methods/{pm_id}", headers=headers)
    list_res = await client.get("/payment-methods/", headers=headers)
    assert len(list_res.json()) == 0
