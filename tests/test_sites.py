import pytest
from tests.utils.testclient import Testclient

def test_create_site_success(client, auth_headers):
    """Test successful site creation."""
    test_client = Testclient(client, auth_headers)
    
    site_data = {
        'name': 'New Hospital Campus',
        'address': '456 Healthcare Ave',
        'city': 'Chicago',
        'country': 'USA',
        'description': 'A new medical facility'
    }
    
    response = test_client.post('/v1/sites', site_data)
    test_client.assert_status(response, 201)
    
    data = test_client.assert_json(response)
    assert data['name'] == site_data['name']
    assert data['address'] == site_data['address']
    assert 'id' in data
    assert 'created_at' in data

def test_create_site_missing_required_fields(client, auth_headers):
    """Test site creation with missing required fields."""
    test_client = Testclient(client, auth_headers)
    
    invalid_data = {'name': 'Incomplete Site'}
    response = test_client.post('/v1/sites', invalid_data)
    test_client.assert_status(response, 400)
    
    data = response.get_json()
    assert 'error' in data
    assert 'required' in data['error'].lower()

def test_get_site_success(client, auth_headers, test_site):
    """Test successful site retrieval."""
    test_client = Testclient(client, auth_headers)
    
    # Use the ID from the fixture (which is a dict)
    response = test_client.get(f'/v1/sites/{test_site["id"]}')
    test_client.assert_status(response, 200)
    
    data = test_client.assert_json(response)
    assert data['id'] == test_site['id']
    assert data['name'] == test_site['name']

def test_get_nonexistent_site(client, auth_headers):
    """Test retrieval of non-existent site."""
    test_client = Testclient(client, auth_headers)
    
    response = test_client.get('/v1/sites/nonexistent-id')
    test_client.assert_status(response, 404)
    
    data = response.get_json()
    assert 'error' in data

def test_delete_site_success(client, auth_headers, test_site):
    """Test successful site deletion."""
    test_client = Testclient(client, auth_headers)
    
    # First verify site exists
    response = test_client.get(f'/v1/sites/{test_site["id"]}')
    test_client.assert_status(response, 200)
    
    # Delete the site
    response = test_client.delete(f'/v1/sites/{test_site["id"]}')
    test_client.assert_status(response, 204)
    
    # Verify site is gone
    response = test_client.get(f'/v1/sites/{test_site["id"]}')
    test_client.assert_status(response, 404)

def test_delete_nonexistent_site(client, auth_headers):
    """Test deletion of non-existent site."""
    test_client = Testclient(client, auth_headers)
    
    response = test_client.delete('/v1/sites/nonexistent-id')
    test_client.assert_status(response, 404)
