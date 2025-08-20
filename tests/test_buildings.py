import pytest
from tests.utils.testclient import Testclient

def test_create_buildings_success(client, auth_headers, test_site):
    """Test successful buildings creation."""
    test_client = Testclient(client, auth_headers)
    
    buildings_data = [
        {
            'name': 'Research Center',
            'code': 'RC',
            'address': '123 Research Dr',
            'floors': 5
        },
        {
            'name': 'Emergency Department',
            'code': 'ED',
            'address': '123 Emergency Dr',
            'floors': 3
        }
    ]
    
    response = test_client.post(f'/v1/sites/{test_site["id"]}/buildings', buildings_data)
    test_client.assert_status(response, 201)
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['name'] == buildings_data[0]['name']
    assert data[1]['name'] == buildings_data[1]['name']

def test_create_buildings_invalid_site(client, auth_headers):
    """Test building creation with invalid site ID."""
    test_client = Testclient(client, auth_headers)
    
    buildings_data = [{
        'name': 'Test Building',
        'code': 'TB',
        'address': '123 Test St',
        'floors': 3
    }]
    
    response = test_client.post('/v1/sites/invalid-site-id/buildings', buildings_data)
    test_client.assert_status(response, 404)

def test_create_buildings_missing_fields(client, auth_headers, test_site):
    """Test building creation with missing required fields."""
    test_client = Testclient(client, auth_headers)
    
    invalid_data = [{'name': 'Incomplete Building'}]
    response = test_client.post(f'/v1/sites/{test_site["id"]}/buildings', invalid_data)
    test_client.assert_status(response, 400)

def test_get_building_success(client, auth_headers, test_building):
    """Test successful building retrieval."""
    test_client = Testclient(client, auth_headers)
    
    response = test_client.get(f'/v1/buildings/{test_building["id"]}')
    test_client.assert_status(response, 200)
    
    data = test_client.assert_json(response)
    assert data['id'] == test_building["id"]
    assert data['name'] == test_building["name"]
    assert data['site_id'] == test_building["site_id"]

def test_get_nonexistent_building(client, auth_headers):
    """Test retrieval of non-existent building."""
    test_client = Testclient(client, auth_headers)
    
    response = test_client.get('/v1/buildings/nonexistent-id')
    test_client.assert_status(response, 404)

def test_delete_building_success(client, auth_headers, test_building):
    """Test successful building deletion."""
    test_client = Testclient(client, auth_headers)
    
    # Verify building exists first
    response = test_client.get(f'/v1/buildings/{test_building["id"]}')
    test_client.assert_status(response, 200)
    
    # Delete the building
    response = test_client.delete(f'/v1/buildings/{test_building["id"]}')
    test_client.assert_status(response, 204)
    
    # Verify building is gone
    response = test_client.get(f'/v1/buildings/{test_building["id"]}')
    test_client.assert_status(response, 404)
