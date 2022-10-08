import pytest

def test_home_endpoint_returns_welcome_page(client):
	response = client.get(path='/')
	assert response.status_code == 200
	assert 'Welcome to TurnPage ! Heaven for Book Lovers' in str(response.content)