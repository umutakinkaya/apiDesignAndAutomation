from flask import Blueprint, request
from app.init import db
from app.models import Site
from app.utils.helpers import (
    validate_required_fields, success_response, error_response, not_found_response
)

sites_bp = Blueprint('sites', __name__)

@sites_bp.route('/sites', methods=['POST'])
def create_site():
    try:
        data = request.get_json()
        
        required_fields = ['name', 'address', 'city', 'country']
        missing_fields = validate_required_fields(data, required_fields)
        
        if missing_fields:
            return error_response(f'Missing required fields: {", ".join(missing_fields)}', 400)
        
        site = Site(
            name=data['name'],
            address=data['address'],
            city=data['city'],
            country=data['country'],
            description=data.get('description', '')
        )
        
        db.session.add(site)
        db.session.commit()
        
        response_data = {
            'id': site.id,
            'name': site.name,
            'address': site.address,
            'city': site.city,
            'country': site.country,
            'description': site.description,
            'created_at': site.created_at.isoformat(),
            'updated_at': site.updated_at.isoformat()
        }
        
        return success_response(response_data, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)

@sites_bp.route('/sites/<site_id>', methods=['GET'])
def get_site(site_id):
    try:
        site = Site.query.get(site_id)
        if not site:
            return not_found_response('Site')
        
        response_data = {
            'id': site.id,
            'name': site.name,
            'address': site.address,
            'city': site.city,
            'country': site.country,
            'description': site.description,
            'created_at': site.created_at.isoformat(),
            'updated_at': site.updated_at.isoformat()
        }
        
        return success_response(response_data)
        
    except Exception as e:
        return error_response(str(e), 500)

@sites_bp.route('/sites/<site_id>', methods=['DELETE'])
def delete_site(site_id):
    try:
        site = Site.query.get(site_id)
        if not site:
            return not_found_response('Site')
        
        db.session.delete(site)
        db.session.commit()
        
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)