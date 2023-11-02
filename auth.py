from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from models import db, Users, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    gmail = data.get('gmail')
    password = data.get('password')

    if not gmail or not password:
        return jsonify({'message': 'gmail and password are required'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = Users(gmail=gmail, password=hashed_password)

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
        user = Users.query.filter_by(gmail=gmail).one()
        if bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid password'}), 401
    except NoResultFound:
        return jsonify({'message': 'User not found'}), 401