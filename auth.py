from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from models import db, User, bcrypt
from helpers import generate_token, validate_token

auth_bp = Blueprint('auth', __name__, url_prefix="/v1/auth")

@auth_bp.route('/register', methods=['POST'])
@validate_token(admin_req=True)
def register(user_id):
    data = request.get_json()
    name = data.get('name')
    gmail = data.get('gmail')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    if any(field is None for field in [name, gmail, password, is_admin, user_id]):
        return jsonify({'message': f'Name, Gmail and Password are required'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, gmail=gmail, is_admin=is_admin,
                    created_by=user_id, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'gmail already exists'}), 400

@auth_bp.route('/login', methods=['POST'])
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
            return jsonify({'message': 'Login successful', 'token': token})
        else:
            return jsonify({'message': 'Invalid password'}), 401
    except NoResultFound:
        return jsonify({'message': 'User not found'}), 401

@auth_bp.route('/profile', methods=['GET', 'POST'])
@validate_token()
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

    try:
        db.session.commit()
        return jsonify({'message': 'User update success'}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({'message': 'Error occurred while updating'}), 400


@auth_bp.route('/all', methods=['GET'])
@validate_token(admin_req=True)
def all(_):
    users = User.query.all()
    return jsonify({'users': [{'id': u.id, 'name': u.name, 'gmail': u.gmail,
                               'is_admin': u.is_admin, 'created_by': u.created_by} for u in users]}), 200