from flask import Blueprint, jsonify
from core.helpers import validate_token
from flasgger import swag_from

reports_bp = Blueprint('reports', __name__, url_prefix='/v1/reports/')

@reports_bp.route('/monthly-events', methods=['GET'])
@validate_token()
@swag_from({
    'summary': 'Endpoint for fetching monthly events.',
    'description': 'Returns a list of monthly events for the authenticated user.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the authenticated user'
        }
    ],
    'responses': {
        200: {
            'description': 'A successful response with monthly events.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {
                                'type': 'string'
                            },
                            'user_id': {
                                'type': 'integer'
                            }
                        }
                    }
                }
            }
        }
    }
})
def monthly_events(user_id):
    return jsonify({'message': 'ok', 'user_id': user_id}), 200

    