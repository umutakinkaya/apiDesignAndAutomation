import factory
from app.models import Site, Building, Level
from app import db

class SiteFactory(factory.Factory):
    class Meta:
        model = Site
    
    id = factory.Faker('uuid4')
    name = factory.Faker('company')
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    country = factory.Faker('country_code')
    description = factory.Faker('text')

class BuildingFactory(factory.Factory):
    class Meta:
        model = Building
    
    id = factory.Faker('uuid4')
    name = factory.Faker('building_name')
    code = factory.Faker('lexify', text='???')
    address = factory.Faker('street_address')
    floors = factory.Faker('random_int', min=1, max=20)

class LevelFactory(factory.Factory):
    class Meta:
        model = Level
    
    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    level_number = factory.Faker('random_int', min=-2, max=10)
    description = factory.Faker('sentence')
    map_data = factory.Faker('text')