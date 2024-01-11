from flask import Blueprint, request, jsonify
from flasgger import swag_from
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from core.models import db, User, bcrypt
from core.token import generate_token, validate_token
from core.mailer import send_email
from circuitbreaker import circuit
from core.logger import logger
from core.util import generate_random_pass, handle_service_unavailable

auth_bp = Blueprint('auth', __name__, url_prefix="/v1/auth")


@auth_bp.route('/register', methods=['POST'])
@validate_token(admin_req=True)
@circuit(failure_threshold=2, expected_exception=Exception,
         recovery_timeout=60, fallback_function=handle_service_unavailable)
@swag_from({
    'summary': 'Endpoint for user registration.',
    'description': 'Register a new user with required details.',
    'responses': {
        201: {
            'description': 'User registered successfully.'
        },
        400: {
            'description': 'Missing required fields or Gmail already exists.'
        }
    }
})
def register(user_id):
    data = request.get_json()
    name = data.get('name')
    gmail = data.get('gmail')
    password = generate_random_pass()
    is_admin = data.get('is_admin', False)

    if any(field is None for field in [name, gmail, is_admin, user_id]):
        return jsonify({'message': f'Name, Gmail are required'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, gmail=gmail, is_admin=is_admin,
                    created_by=user_id, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        send_email(
            gmail,
            'Welcome to WorkClock',
            f'Hi {gmail},\n\nWelcome to WorkClock!\nYour password is {password}\n\nRegards,\nWorkClock team'
        )
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'gmail already exists'}), 400


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'summary': 'Endpoint for user login.',
    'description': 'Authenticate a user with Gmail and password.',
    'responses': {
        200: {
            'description': 'Login successful.',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string'},
                            'token': {'type': 'string'}
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Invalid credentials or user not found.'
        }
    }
})
def login():
    data = request.get_json()
    gmail = data.get('gmail')
    password = data.get('password')

    if not gmail or not password:
        return jsonify({'message': 'gmail and password are required'}), 400

    try:
        user = User.query.filter_by(gmail=gmail).first()
        if user and bcrypt.check_password_hash(user.password, password):
            token = generate_token(user.id, user.is_admin)
            logger.info(f'User login success {gmail}')
            return jsonify({'message': 'Login successful', 'token': token, 'is_admin': user.is_admin})
        else:
            logger.error(f'Login with gmail {gmail} failed!')
            return jsonify({'message': 'Invalid password'}), 401
    except NoResultFound:
        return jsonify({'message': 'User not found'}), 401


@auth_bp.route('/profile', methods=['GET', 'POST'])
@validate_token()
@swag_from({
    'summary': 'Endpoint for user profile management.',
    'description': 'View or update user profile details.',
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
            'description': 'User details retrieved successfully or updated successfully.'
        },
        400: {
            'description': 'Error occurred while updating user details.'
        },
        404: {
            'description': 'User not found.'
        }
    }
})
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({'id': user.id, 'gmail': user.gmail, 'name': user.name, 'is_admin': user.is_admin}), 200

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.gmail = data.get('gmail', user.gmail)
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8') if data.get('password') else user.password
    user.password = hashed_password
    logger.info(f'User {user.id} was updated with data name: {user.name}, gmail: {user.gmail}')

    try:
        db.session.commit()
        return jsonify({'message': 'User update success'}), 200
    except Exception as ex:
        logger.error(str(ex))
        db.session.rollback()
        return jsonify({'message': 'Error occurred while updating'}), 400


@auth_bp.route('/all', methods=['GET'])
@validate_token(admin_req=True)
@swag_from({
    'summary': 'Endpoint to fetch all users.',
    'description': 'Retrieve details of all registered users.',
    'responses': {
        200: {
            'description': 'All users retrieved successfully.'
        }
    }
})
def get_all(_):
    users = User.query.all()
    logger.info(f'All users were fetched count: {len(users)}')
    return jsonify({'users': [{'id': u.id, 'name': u.name, 'gmail': u.gmail,
                               'is_admin': u.is_admin, 'created_by': u.created_by} for u in users]}), 200


@auth_bp.route('/remove-user', methods=['DELETE'])
@validate_token(admin_req=True)
@swag_from({
    'summary': 'Endpoint to remove a user.',
    'description': 'Delete an existing user by user_id.',
    'responses': {
        200: {
            'description': 'User deleted successfully.'
        },
        400: {
            'description': 'Invalid user_id or deletion failed.'
        }
    }
})
def remove_user(_):
    user_id = request.args.get('id')

    if user_id is None:
        return jsonify({'message': 'User ID is required'}), 400

    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        except Exception as e:
            logger.error(str(e))
            db.session.rollback()
            return jsonify({'message': 'Deletion failed'}), 400
    else:
        return jsonify({'message': 'Invalid user ID'}), 400



@auth_bp.route('/user', methods=['GET', 'POST'])
@validate_token(admin_req=True)
@swag_from({
    'summary': 'Endpoint for user profile management (Admins).',
    'description': 'View or update user profile details.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the authenticated user'
        },
    ],
    'responses': {
        200: {
            'description': 'User details retrieved successfully or updated successfully.'
        },
        400: {
            'description': 'Error occurred while updating user details.'
        },
        404: {
            'description': 'User not found.'
        }
    }
})
def admin_user_action(_):
    user_id = request.args.get('id')
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({'id': user.id, 'gmail': user.gmail, 'name': user.name, 'is_admin': user.is_admin}), 200
    
    req_json = request.get_json()
    data = {
        'name': req_json.get('name', user.name),
        'gmail': req_json.get('gmail', user.gmail),
        'password': req_json.get('password')
    }
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8') if data.get('password') else user.password
    user.name = data['name']
    user.gmail = data['gmail']
    user.password = hashed_password
    logger.info(f'User {user.id} was updated with data name: {user.name}, gmail: {user.gmail}')

    try:
        db.session.commit()
        return jsonify({'message': 'User update success'}), 200
    except Exception as ex:
        logger.error(str(ex))
        db.session.rollback()
        return jsonify({'message': 'Error occurred while updating'}), 400