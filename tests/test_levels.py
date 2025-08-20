import pytest
import base64
from tests.utils.testclient import Testclient

def test_create_levels_success(client, auth_headers, test_building):
    """Test successful levels creation."""
    test_client = Testclient(client, auth_headers)
    
    map_data = base64.b64encode(b'test map data').decode('utf-8')
    levels_data = [
        {
            'name': 'Ground Floor',
            'level_number': "0",
            'description': 'Main entrance level',
            'map_data': map_data
        },
        {
            'name': 'First Floor',
            'level_number': "1",
            'description': 'Patient rooms level',
            'map_data': map_data
        }
    ]
    
    response = test_client.post(f'/v1/buildings/{test_building["id"]}/levels', levels_data)
    test_client.assert_status(response, 201)
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['level_number'] == 0
    assert data[1]['level_number'] == 1

def test_create_single_level(client, auth_headers, test_building):
    """Test creating a single level."""
    test_client = Testclient(client, auth_headers)
    
    level_data = [{
        'name': 'Basement',
        'level_number': -1,
        'description': 'Storage and utilities'
    }]
    
    response = test_client.post(f'/v1/buildings/{test_building["id"]}/levels', level_data)
    test_client.assert_status(response, 201)
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'Basement'

def test_create_levels_invalid_building(client, auth_headers):
    """Test level creation with invalid building ID."""
    test_client = Testclient(client, auth_headers)
    
    levels_data = [{
        'name': 'Test Level',
        'level_number': 1,
        'description': 'Test description'
    }]
    
    response = test_client.post('/v1/buildings/invalid-building-id/levels', levels_data)
    test_client.assert_status(response, 404)

def test_create_levels_missing_fields(client, auth_headers, test_building):
    """Test level creation with missing required fields."""
    test_client = Testclient(client, auth_headers)
    
    invalid_data = [{'name': 'Incomplete Level'}]
    response = test_client.post(f'/v1/buildings/{test_building["id"]}/levels', invalid_data)
    test_client.assert_status(response, 400)
