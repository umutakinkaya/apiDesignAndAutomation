import tempfile
import pytest
import os
import sys
from app.init import create_app, db
from app.models import Site, Building, Level

# Add the app directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for tests with Test database."""
    # Use the same database as the main app
    # Create a temporary test database file
 

    # Set environment to use the real database
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['AUTH_TOKENS'] = 'test-token'
    os.environ['FLASK_ENV'] = 'testing'


    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_headers():
    """Default authentication headers."""
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json'
    }

@pytest.fixture
def test_site(app):
    """Create a test site and return only the ID."""
    with app.app_context():
        site = Site(
            name='Test Hospital Campus',
            address='123 Medical Center Dr',
            city='Boston',
            country='USA',
            description='Test hospital campus'
        )
        db.session.add(site)
        db.session.commit()
        
        # Return only the ID and basic info to avoid detached instance issues
        return {'id': site.id, 'name': site.name}

@pytest.fixture
def test_building(app, test_site):
    """Create a test building."""
    with app.app_context():
        # Get the site within the current session
        site = db.session.get(Site, test_site['id'])
        building = Building(
            name='Main Hospital Building',
            code='MHB',
            address='123 Medical Center Dr, Building A',
            floors=10,
            site_id=site.id
        )
        db.session.add(building)
        db.session.commit()
        return {'id': building.id, 'name': building.name, 'site_id': building.site_id}

@pytest.fixture
def test_level(app, test_building):
    """Create a test level."""
    with app.app_context():
        building = db.session.get(Building, test_building['id'])
        level = Level(
            name='Ground Floor',
            level_number=0,
            description='Main entrance and reception',
            map_data='base64_encoded_data',
            building_id=building.id
        )
        db.session.add(level)
        db.session.commit()
        return {'id': level.id, 'name': level.name, 'building_id': level.building_id}