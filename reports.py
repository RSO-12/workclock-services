from flask import Blueprint, request, jsonify
from helpers import validate_token

reports_bp = Blueprint('reports', __name__, url_prefix='/v1/reports/')

@reports_bp.route('/monthly-events', methods=['GET'])
@validate_token()
def monthly_events(user_id):
    return jsonify({'message': 'ok', 'user_id': user_id}), 200

    