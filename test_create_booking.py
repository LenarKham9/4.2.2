from constant import BASE_URL
import requests



def test_create_booking(auth_session, booking_data):
    create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    assert create_booking.status_code == 200, "Ошибка при создании брони"
    booking_id = create_booking.json().get("bookingid")
    assert booking_id is not None, "Идентификатор брони не найден в ответе"
    assert create_booking.json()["booking"]["firstname"] == booking_data['firstname'], "Заданное имя не совпадает"
    assert create_booking.json()["booking"]["totalprice"] == booking_data['totalprice'], "Заданная стоимость не совпадает"
    get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert get_booking.status_code == 200, "Бронь не найдена"
    assert get_booking.json()["lastname"] == booking_data['lastname'], "Заданная фамилия не совпадает"

    deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
    assert deleted_booking.status_code == 201, "Бронь не удалилась"

    get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert get_booking.status_code == 404, "Бронь не удалилась"



def test_get_all_bookings(auth_session):
    response = auth_session.get(f"{BASE_URL}/booking")
    assert response.status_code == 200

    # Тест на обновление бронирования (PUT)
def test_update_booking(auth_session, created_booking, booking_data):
        # Новые данные для обновления
    updated_data = booking_data.copy()
    updated_data["firstname"] = "UpdatedName"
    updated_data["lastname"] = "UpdatedLastName"
        # Обновление бронирования
    response = auth_session.put(f"{BASE_URL}/booking/{created_booking}", json=updated_data)
    assert response.status_code == 200

        # Проверка обновления
    get_response = auth_session.get(f"{BASE_URL}/booking/{created_booking}")
    assert get_response.status_code == 200
    booking = get_response.json()
    assert booking["firstname"] == "UpdatedName"
    assert booking["lastname"] == "UpdatedLastName"


# Тест на частичное обновление бронирования (PATCH)
def test_partial_update_booking(auth_session, created_booking):
    # Данные для частичного обновления
    patch_data = {
        "firstname": "PatchedName",
        "additionalneeds": "Dinner"
        }

    # Частичное обновление
    response = auth_session.patch(f"{BASE_URL}/booking/{created_booking}",
        json=patch_data)
    assert response.status_code == 200

    # Проверка обновления
    get_response = auth_session.get(f"{BASE_URL}/booking/{created_booking}")
    assert get_response.status_code == 200
    booking = get_response.json()
    assert booking["firstname"] == "PatchedName"
    assert booking["additionalneeds"] == "Dinner"


# Тест на получение бронирования по ID
def test_get_booking_by_id(auth_session, created_booking, booking_data):
    response = auth_session.get(f"{BASE_URL}/booking/{created_booking}")
    assert response.status_code == 200
    booking = response.json()
    assert booking["firstname"] == booking_data["firstname"]
    assert booking["lastname"] == booking_data["lastname"]


# Тест на попытку получения несуществующего бронирования
def test_get_nonexistent_booking(auth_session):
    response = auth_session.get(f"{BASE_URL}/booking/999999")
    assert response.status_code == 404


# Тест на создание бронирования с неполными данными
def test_create_booking_with_invalid_data(auth_session):
    invalid_data = {
        "firstname": "Test",
        "lastname": "User"
        # Отсутствуют обязательные поля
        }
    response = auth_session.post(f"{BASE_URL}/booking", json=invalid_data)
    assert response.status_code == 500


# Тест на обновление бронирования без авторизации
def test_update_booking_unauthorized(booking_data, created_booking):
    session = requests.Session()
    updated_data = booking_data.copy()
    updated_data["firstname"] = "UnauthorizedUpdate"

    response = session.put(
        f"{BASE_URL}/booking/{created_booking}",
        json=updated_data)
    assert response.status_code == 403



