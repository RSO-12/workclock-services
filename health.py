from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__, url_prefix="/v1/health")

@health_bp.route('/ready')
def readiness():
    """
    Endpoint for Kubernetes readiness probe.

    Returns a 200 OK response if the application is ready.
    """
    return jsonify({'status': 'ok'})

@health_bp.route('/live')
def liveness():
    """
    Endpoint for Kubernetes liveness probe.

    Returns a 200 OK response if the application is alive.
    """
    return jsonify({'status': 'alive'})