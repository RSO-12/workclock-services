from flask import Blueprint, jsonify
from core.token import validate_token

mock_bp = Blueprint('mock', __name__, url_prefix='/v1/mock/')


@mock_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'ok': True})


@mock_bp.route('/token-test', methods=['GET'])
@validate_token()
def token_test(user_id):
    return jsonify({'user': user_id})


@mock_bp.route('/token-admin-test', methods=['GET'])
@validate_token(admin_req=True)
def token_admin_test(user_id):
    return jsonify({ 'user': user_id })
