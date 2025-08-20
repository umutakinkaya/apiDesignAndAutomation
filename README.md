# **Pointr REST API and Automated Test**
A comprehensive RESTful API for managing sites, buildings, and levels with full test automation and CI/CD pipeline.

🚀**Features**

- RESTful API with proper HTTP status codes

- SQLite/PostgreSQL database support

- Comprehensive Testing with pytest

- CI/CD Pipeline with Jenkins

📋 **API Endpoints**

**Sites API**

POST /v1/sites - Create a new site

GET /v1/sites/{id} - Get a specific site

DELETE /v1/sites/{id} - Delete a site


------------


**Buildings API**

POST /v1/sites/{site_id}/buildings - Create buildings for a site

GET /v1/buildings/{id} - Get a specific building

DELETE /v1/buildings/{id} - Delete a building


------------


**Levels API**

POST /v1/buildings/{building_id}/levels - Create levels for a building



------------



**🛠️ Installation**

**Prerequisites**

Python 3.9+

PostgreSQL (optional, SQLite included in the project)


**Local Development**

Clone the repository

git clone https://github.com/yourusername/apiDesignAndAutomation.git

cd apiDesignAndAutomation

python runAPI.py

The API will be available at http://localhost:5000

"Usage: python runAPI.py [init-db|seed-db|run]"

init-db : create tables for the API

seed-db : creates test data for database

run     : just runs API

If you dont use any run parameter, runAPI will run all parameters. 




** Database**
DATABASE_URL=sqlite:///pointr.db


------------



**🧪 Testing**

**Run All Tests**

python -m pytest tests/ -v

*for detail test report RUN*: 
python -m pytest tests/ -v --html=test-results/detailed-report.html --self-contained-html

**Run Specific Test Groups**

**Site tests**
python -m pytest tests/test_sites.py -v

**Building tests**
python -m pytest tests/test_buildings.py -v

**Level tests**
python -m pytest tests/test_levels.py -v


------------



**Test with Different Databases**
**SQLite in-memory (default)**
python -m pytest tests/ -v
**PostgreSQL**
DATABASE_URL=postgresql://user:pass@localhost:5432/testdb python -m pytest tests/ -v


**📊 API Usage Examples**

curl -H "Authorization: Bearer test-token" http://localhost:5000/v1/sites

curl -X POST http://localhost:5000/v1/sites \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Sitesi",
    "address": "123 Sokak Test Adresi",
    "city": "İstanbul",
    "country": "TR",
    "description": "Bir sürü binası olan büyük bir site"
  }'
Create Buildings

curl -X POST http://localhost:5000/v1/sites/{site_id}/buildings \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "name": "Site binaA",
      "code": "AAA",
      "address": "123 SOkak St",
      "floors": 10
    }
  ]'


curl -X POST http://localhost:5000/v1/buildings/{building_id}/levels \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "name": "Zemin kat",
      "level_number": 0,
      "description": "Giriş",
      "map_data": "base64_encoded_data"
    }
  ]'


------------



📈 CI/CD Pipeline

- The project includes a complete Jenkins CI/CD pipeline:

- Pipeline Stages

- Checkout - Source code checkout

- Setup - Dependency installation
- Lint - Code quality checking

- Test - Unit and integration tests

- Coverage - Test coverage reporting

- Build - Docker image building

- Deploy - Production deployment


------------


#Requirements
**Core Framework**
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
SQLAlchemy==2.0.32
python-dotenv==1.0.0

**Testing**
pytest==8.4.1
pytest-cov==4.1.0
pytest-html==4.1.1
pytest-xdist==3.3.1
Faker==25.8.0
factory-boy==3.3.1
requests==2.31.0

**Package Management**
pip-tools==6.13.0
