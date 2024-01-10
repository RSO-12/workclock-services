from flask import Blueprint, jsonify
from circuitbreaker import circuit

fault_demo_bp = Blueprint('reports', __name__, url_prefix='/v1/fault/')


@fault_demo_bp.route('/demo', methods=['GET'])
@circuit
def monthly_events():
    return jsonify({ 'Worked': True })