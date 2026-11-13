import os

os.environ["DATABASE_URL"] = "sqlite://"  # in-memory; set before the app imports the engine

import pytest
from fastapi.testclient import TestClient

from coffee_pos.db import Base, engine
from coffee_pos.main import app


@pytest.fixture
def client():
    Base.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(engine)


def add_item(client, name="Latte", price="65.00"):
    r = client.post("/menu", json={"name": name, "price": price})
    assert r.status_code == 201
    return r.json()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_menu_starts_empty(client):
    assert client.get("/menu").json() == []


def test_create_and_list_menu_item(client):
    item = add_item(client)
    assert item["name"] == "Latte"
    assert item["price"] == "65.00"
    assert client.get("/menu").json() == [item]


def test_menu_rejects_negative_price(client):
    r = client.post("/menu", json={"name": "Free", "price": "-1"})
    assert r.status_code == 422


def test_menu_rejects_duplicate_name(client):
    add_item(client)
    r = client.post("/menu", json={"name": "Latte", "price": "70.00"})
    assert r.status_code == 409


def test_create_order_computes_total(client):
    latte = add_item(client, "Latte", "65.00")
    mocha = add_item(client, "Mocha", "70.50")
    r = client.post(
        "/orders",
        json={"items": [{"menu_item_id": latte["id"], "quantity": 2}, {"menu_item_id": mocha["id"], "quantity": 1}]},
    )
    assert r.status_code == 201
    order = r.json()
    assert order["total"] == "200.50"
    assert client.get(f"/orders/{order['id']}").json() == order


def test_order_unknown_item_404(client):
    r = client.post("/orders", json={"items": [{"menu_item_id": 999, "quantity": 1}]})
    assert r.status_code == 404


def test_order_rejects_zero_quantity_and_empty(client):
    latte = add_item(client)
    assert client.post("/orders", json={"items": [{"menu_item_id": latte["id"], "quantity": 0}]}).status_code == 422
    assert client.post("/orders", json={"items": []}).status_code == 422


def test_get_missing_order_404(client):
    assert client.get("/orders/999").status_code == 404


def test_metrics_exposed(client):
    client.get("/health")
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "http_requests_total" in r.text
