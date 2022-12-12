from fastapi.testclient import TestClient
from .app import app
import pytest
from httpx import AsyncClient


class MockResponse:
    
    @staticmethod
    def json():
        return {'beans': 10, 'water': 20}
    
    status_code: int = 200


client = TestClient(app)


def test_get_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'hello world'}
    

@pytest.mark.anyio
async def test_get_levels(monkeypatch):
    test_response_payload = {'beans': 10, 'water': 20}
 
    async def mock_get_levels(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr(client, 'get', mock_get_levels)
    
    response = await client.get('/levels')
    assert response.status_code == 200
    assert response.json() == test_response_payload
    
    
@pytest.mark.anyio
async def test_post_brew(monkeypatch):
    test_response_payload = {'beans': 10, 'water': 20}
 
    async def mock_post_brew(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr(client, 'get', mock_post_brew)
    
    response = await client.get('/levels')
    assert response.status_code == 200
    assert response.json() == test_response_payload