import jwt
import os
from datetime import datetime, timedelta
from flask import jsonify, request
from functools import wraps

JWT_SECRET = os.environ.get('JWT_SECRET', 'default_value')

def generate_token(user_id, is_admin, expiration_minutes=60 * 8):
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(minutes=expiration_minutes)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token

def validate_token(admin_req=False):

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 401

            try:
                jwt_token = token[7:]
                payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=['HS256'])
                user_id = payload.get('user_id')
                if admin_req and not payload.get('is_admin'):
                    return jsonify({'message': 'Admin required for this action'}), 403

                return f(user_id, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidSignatureError:
                return jsonify({'message': 'Invalid token'}), 401

        return wrapper
    return decorator