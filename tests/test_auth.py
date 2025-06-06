import pytest

#REGISTER

@pytest.mark.asyncio
async def test_register_success(async_client):
    payload = {
        "email": "test_register_success@mail.com",
        "password": "12345678",
        "confirm_password": "12345678"
    }
    response = await async_client.post("/auth/register", json=payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_register_and_unique_email(async_client):
    payload = {
        "email": "test_register_and_unique_email@admin.com",
        "password": "password123",
        "confirm_password": "password123"
    }

    response1 = await async_client.post("/auth/register", json=payload)
    assert response1.status_code == 200

    response2 = await async_client.post("/auth/register", json=payload)
    assert response2.status_code == 409

@pytest.mark.asyncio
async def test_register_passwords_dismatch(async_client):
    payload = {
        "email": "test_register_passwords_dismatch@admin.com",
        "password": "12345678",
        "confirm_password": "123456789"
    }

    response = await async_client.post("auth/register", json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_validation_errors(async_client):
    valid_user = {
    "email": "test_register_validation_errors@admin.com",
    "password": "12345678",
    "confirm_password": "12345678"
    }
    response = await async_client.post("/auth/register", json=valid_user)
    assert response.status_code == 200

    invalid_email_user = valid_user.copy()
    invalid_email_user["email"] = "not-an-email"
    response = await async_client.post("/auth/register", json=invalid_email_user)
    assert response.status_code == 422

    short_password_user = valid_user.copy()
    short_password_user["password"] = "123"
    short_password_user["confirm_password"] = "123"
    response = await async_client.post("/auth/register", json=short_password_user)
    assert response.status_code == 422

    long_password = "a" * 129
    long_password_user = valid_user.copy()
    long_password_user["password"] = long_password
    long_password_user["confirm_password"] = long_password
    response = await async_client.post("/auth/register", json=long_password_user)
    assert response.status_code == 422

#LOGIN

@pytest.mark.asyncio
async def test_login_success(async_client):
    payload = {
        "email": "test_login_success@mail.com",
        "password": "12345678",
        "confirm_password": "12345678"
    }
    await async_client.post("/auth/register", json=payload)

    payload.pop('confirm_password', None)
    response = await async_client.post('/auth/login', json=payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    payload = {
        "email": "test_login_user_not_found@mail.com",
        "password": "12345678"
    }

    response = await async_client.post("/auth/login", json=payload)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_login_wrong_password(async_client):
    payload = {
        "email": "test_login_wrong_password@mail.com",
        "password": "12345678",
        "confirm_password": "12345678"
    }
    await async_client.post("/auth/register", json=payload)

    payload["password"] = "wrongpassword"
    payload.pop("confirm_password", None)

    response = await async_client.post("/auth/login", json=payload)
    assert response.status_code == 401