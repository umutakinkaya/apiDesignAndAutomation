import pytest
from tests.utils.testclient import Testclient

def test_invalid_json(client, auth_headers):
    """Test sending invalid JSON."""
    test_client = Testclient(client, auth_headers)
    
    # Send malformed JSON
    response = test_client.post(
        '/v1/sites',
        data='{invalid json',
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_invalid_content_type(client, auth_headers):
    """Test sending wrong content type."""
    test_client = Testclient(client, auth_headers)
    
    site_data = {
        'name': 'Test Site',
        'address': '123 Test St',
        'city': 'Test City',
        'country': 'Test Country'
    }
    
    # Send with wrong content type
    headers = auth_headers.copy()
    headers['Content-Type'] = 'text/plain'
    
    response = test_client.post(
        '/v1/sites',
        data=str(site_data),
        headers=headers
    )
    
    assert response.status_code == 500
    assert 'error' in response.get_json()

def test_nonexistent_endpoint(client, auth_headers):
    """Test accessing non-existent endpoint."""
    test_client = Testclient(client, auth_headers)
    
    response = test_client.get('/v1/nonexistent')
    assert response.status_code == 404

def test_method_not_allowed(client, auth_headers):
    """Test using wrong HTTP method."""
    test_client = Testclient(client, auth_headers)
    
    # Try to POST to a GET endpoint
    response = test_client.post('/v1/sites/some-id')
    assert response.status_code == 405