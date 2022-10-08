import pytest


def test_home_endpoint_returns_welcome_page(client):
    response = client.get(path='/')
    assert response.status_code == 200
