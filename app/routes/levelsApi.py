from flask import Blueprint, request
from app.init import db
from app.models import Building, Level
from app.utils.helpers import (
    validate_required_fields, success_response, error_response, not_found_response
)

levels_bp = Blueprint('levels', __name__)

@levels_bp.route('/buildings/<building_id>/levels', methods=['POST'])
def create_levels(building_id):
    try:
        building = Building.query.get(building_id)
        if not building:
            return not_found_response('Building')
        
        data = request.get_json()
        if not isinstance(data, list):
            return error_response('Expected an array of levels', 400)
        
        levels = []
        for level_data in data:
            required_fields = ['name', 'level_number']
            missing_fields = validate_required_fields(level_data, required_fields)
            
            if missing_fields:
                return error_response(f'Missing required fields in level: {", ".join(missing_fields)}', 400)
            
            level = Level(
                name=level_data['name'],
                level_number=level_data['level_number'],
                description=level_data.get('description', ''),
                map_data=level_data.get('map_data', ''),
                building_id=building_id
            )
            db.session.add(level)
            levels.append(level)
        
        db.session.commit()
        
        response_data = []
        for level in levels:
            response_data.append({
                'id': level.id,
                'name': level.name,
                'level_number': level.level_number,
                'description': level.description,
                'map_data': level.map_data,
                'building_id': level.building_id,
                'created_at': level.created_at.isoformat(),
                'updated_at': level.updated_at.isoformat()
            })
        
        return success_response(response_data, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)