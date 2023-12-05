from flask import Blueprint, jsonify

metrics_bp = Blueprint('metrics', __name__, url_prefix="/v1/metrics")

@metrics_bp.route('/test')
def test():
    """
    Endpoint for metrics.

    Returns a 200 OK response for now.
    """
    return jsonify({'status': 'ok'})
