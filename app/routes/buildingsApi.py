from flask import Blueprint, request
from app.init import db
from app.models import Site, Building
from app.utils.helpers import (
    validate_required_fields, success_response, error_response, not_found_response
)

buildings_bp = Blueprint('buildings', __name__)

@buildings_bp.route('/sites/<site_id>/buildings', methods=['POST'])
def create_buildings(site_id):
    try:
        site = Site.query.get(site_id)
        if not site:
            return not_found_response('Site')
        
        data = request.get_json()
        if not isinstance(data, list):
            return error_response('Expected an array of buildings', 400)
        
        buildings = []
        for building_data in data:
            required_fields = ['name', 'code', 'address', 'floors']
            missing_fields = validate_required_fields(building_data, required_fields)
            
            if missing_fields:
                return error_response(f'Missing required fields in building: {", ".join(missing_fields)}', 400)
            
            building = Building(
                name=building_data['name'],
                code=building_data['code'],
                address=building_data['address'],
                floors=building_data['floors'],
                site_id=site_id
            )
            db.session.add(building)
            buildings.append(building)
        
        db.session.commit()
        
        response_data = []
        for building in buildings:
            response_data.append({
                'id': building.id,
                'name': building.name,
                'code': building.code,
                'address': building.address,
                'floors': building.floors,
                'site_id': building.site_id,
                'created_at': building.created_at.isoformat(),
                'updated_at': building.updated_at.isoformat()
            })
        
        return success_response(response_data, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)

@buildings_bp.route('/buildings/<building_id>', methods=['GET'])
def get_building(building_id):
    try:
        building = Building.query.get(building_id)
        if not building:
            return not_found_response('Building')
        
        response_data = {
            'id': building.id,
            'name': building.name,
            'code': building.code,
            'address': building.address,
            'floors': building.floors,
            'site_id': building.site_id,
            'created_at': building.created_at.isoformat(),
            'updated_at': building.updated_at.isoformat()
        }
        
        return success_response(response_data)
        
    except Exception as e:
        return error_response(str(e), 500)

@buildings_bp.route('/buildings/<building_id>', methods=['DELETE'])
def delete_building(building_id):
    try:
        building = Building.query.get(building_id)
        if not building:
            return not_found_response('Building')
        
        db.session.delete(building)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)