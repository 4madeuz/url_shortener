import pytest

from httpx import Client
from src.models.url_models import URL

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_urls(test_client: Client, sample_url: URL):
    response = test_client.get('/shortener')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_url(test_client: Client):
    data = {'original_url': '/some/url'}
    response = test_client.post('/shortener', json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert 'id' in response_data
    assert response_data['original_url'] == '/some/url'
    assert 'short_url' in response_data


@pytest.mark.asyncio
async def test_get_short_url(test_client: Client, sample_url: URL):
    response = test_client.get(f'/shortener/{sample_url.short_url}/')
    assert response.url == sample_url.original_url


@pytest.mark.asyncio
async def test_get_by_id(test_client: Client, sample_url: URL):
    response = test_client.get(f'/shortener/info/{sample_url.id}')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == str(sample_url.id)
    assert response_data['short_url'] == sample_url.short_url
    assert response_data['original_url'] == sample_url.original_url
