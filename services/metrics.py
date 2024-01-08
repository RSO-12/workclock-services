from flask import Blueprint, jsonify, Response
from prometheus_client import generate_latest

metrics_bp = Blueprint('metrics', __name__, url_prefix="/v1/metrics")

@metrics_bp.route('/test')
def test():
    """
    Endpoint for metrics.

    Returns a 200 OK response for now.
    """
    return jsonify({'status': 'ok'})


@metrics_bp.route('/')
def metrics():
    return Response(generate_latest(), mimetype="text/plain")
