async def test_create_table(client):
    """Тест на создание столика"""
    response = await client.post(
        "/tables/", json={"name": "Test Table", "seats": 2, "location": "window"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Table"
    assert data["seats"] == 2
    assert data["location"] == "window"


async def test_get_tables(client):
    """Тест на получение списка всех столиков"""

    await client.post(
        "/tables/", json={"name": "Test Table 1", "seats": 2, "location": "window"}
    )
    await client.post(
        "/tables/", json={"name": "Test Table 2", "seats": 4, "location": "terrace"}
    )

    response = await client.get("/tables/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(table["name"] == "Test Table 1" for table in data)
    assert any(table["name"] == "Test Table 2" for table in data)


async def test_delete_table(client):
    """Тест на удаление столика"""
    response = await client.post(
        "/tables/", json={"name": "Table to Delete", "seats": 4, "location": "patio"}
    )
    table_id = response.json()["id"]

    response = await client.delete(f"/tables/{table_id}")
    assert response.status_code == 204

    response = await client.get(f"/tables/{table_id}")
    assert response.status_code == 405  # Столик не найден


async def test_delete_non_existent_table(client):
    """Тест на попытку удаления несуществующего столика"""
    response = await client.delete("/tables/99999")
    assert response.status_code == 404


async def test_create_table_invalid_data(client):
    """Тест на создание столика с некорректными данными"""

    response = await client.post("/tables/", json={"seats": 2, "location": "test"})
    assert response.status_code == 422


async def test_create_table_with_invalid_seats(client):
    """Тест на создание столика с некорректным значением seats"""
    response = await client.post(
        "/tables/", json={"name": "Invalid Table", "seats": -1, "location": "test"}
    )
    assert response.status_code == 422


async def test_get_empty_table_list(client):
    """Тест на получение пустого списка столиков"""
    response = await client.get("/tables/")
    assert response.status_code == 200
    assert response.json() == []
