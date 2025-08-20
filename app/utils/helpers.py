from flask import jsonify

def validate_required_fields(data, required_fields):
    """Validate required fields in request data"""
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    return missing_fields

def success_response(data, status_code=200):
    """Standard success response"""
    return jsonify(data), status_code

def error_response(message, status_code=400):
    """Standard error response"""
    return jsonify({'error': message}), status_code

def not_found_response(resource_name):
    """Standard not found response"""
    return error_response(f'{resource_name} not found', 404)