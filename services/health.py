from flask import Blueprint, jsonify
from flasgger import swag_from

health_bp = Blueprint('health', __name__, url_prefix="/v1/health")

@health_bp.route('/ready')
@swag_from({
    'summary': 'Endpoint for Kubernetes readiness probe.',
    'description': 'Returns a 200 OK response if the application is ready.',
    'responses': {
        200: {
            'description': 'A successful readiness response.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        }
    }
})
def readiness():
    return jsonify({'status': 'ok'})

@health_bp.route('/live')
@swag_from({
    'summary': 'Endpoint for Kubernetes liveness probe.',
    'description': 'Returns a 200 OK response if the application is alive.',
    'responses': {
        200: {
            'description': 'A successful liveness response.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'status': {
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        }
    }
})
def liveness():
    return jsonify({'status': 'alive'})


@health_bp.route('/heartbeat')
@swag_from({
    'summary': 'Endpoint for checking the heartbeat of the service.',
    'description': 'This endpoint returns a simple "Hello World!" message.',
    'responses': {
        200: {
            'description': 'A successful heartbeat response.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'Hello': {
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        }
    }
})
def heartbeat():
    return jsonify({'Hello': 'World!'})