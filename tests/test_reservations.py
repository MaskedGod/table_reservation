from datetime import datetime, timedelta


async def test_create_reservation_success(client):
    """Тест на успешное создание бронирования"""
    response = await client.post(
        "/tables/", json={"name": "Test Table", "seats": 2, "location": "test"}
    )
    assert response.status_code == 201
    table_id = response.json()["id"]

    now = datetime.now()
    reservation_data = {
        "customer_name": "John Doe",
        "table_id": table_id,
        "reservation_time": now.isoformat(),
        "duration_minutes": 60,
    }

    response = await client.post("/reservations/", json=reservation_data)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["table_id"] == table_id
    assert "id" in data


async def test_create_reservation_conflict(client):
    """Тест на конфликт бронирования"""
    response = await client.post(
        "/tables/", json={"name": "Conflict Table", "seats": 2, "location": "window"}
    )
    table_id = response.json()["id"]

    now = datetime.now()
    reservation_time = now.replace(microsecond=0)

    await client.post(
        "/reservations/",
        json={
            "customer_name": "Alice",
            "table_id": table_id,
            "reservation_time": reservation_time.isoformat(),
            "duration_minutes": 60,
        },
    )

    response = await client.post(
        "/reservations/",
        json={
            "customer_name": "Bob",
            "table_id": table_id,
            "reservation_time": (reservation_time + timedelta(minutes=30)).isoformat(),
            "duration_minutes": 60,
        },
    )
    assert response.status_code == 409


async def test_get_reservations_empty(client):
    """Тест на получение пустого списка бронирований"""
    response = await client.get("/reservations/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_reservations(client):
    """Тест на получение списка бронирований"""

    response = await client.post(
        "/tables/", json={"name": "Test Table", "seats": 2, "location": "test"}
    )
    table_id = response.json()["id"]

    now = datetime.now()
    reservation_data = {
        "customer_name": "John Doe",
        "table_id": table_id,
        "reservation_time": now.isoformat(),
        "duration_minutes": 60,
    }

    await client.post("/reservations/", json=reservation_data)

    response = await client.get("/reservations/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["customer_name"] == "John Doe"


async def test_delete_reservation_success(client):
    """Тест на успешное удаление бронирования"""

    response = await client.post(
        "/tables/", json={"name": "Test Table", "seats": 2, "location": "test"}
    )
    table_id = response.json()["id"]

    now = datetime.now()
    reservation_data = {
        "customer_name": "John Doe",
        "table_id": table_id,
        "reservation_time": now.isoformat(),
        "duration_minutes": 60,
    }
    response = await client.post("/reservations/", json=reservation_data)
    reservation_id = response.json()["id"]

    response = await client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 204

    response = await client.get("/reservations/")
    assert len(response.json()) == 0


async def test_delete_reservation_not_found(client):
    """Тест на попытку удаления несуществующего бронирования"""
    response = await client.delete("/reservations/9999999")
    assert response.status_code == 404
