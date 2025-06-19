import pytest
import requests
from faker import Faker

from constant import HEADERS, BASE_URL

faker = Faker()


@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    # Получение токена авторизации
    auth_data = {
        "username": "admin",
        "password": "password123"
        }
    response = session.post(f"{BASE_URL}/auth", json=auth_data)
    token = response.json().get("token")

    # Добавление токена в заголовки сессии
    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture()
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
        }

@pytest.fixture()
def created_booking(auth_session, booking_data):
    # Создание бронирования и возврат его ID
    response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    assert response.status_code == 200
    booking_id = response.json().get("bookingid")
    yield booking_id

    # Удаление бронирования после теста
    auth_session.delete(f"{BASE_URL}/booking/{booking_id}")