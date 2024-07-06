from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User
from app import db

bp =Blueprint('auth', __name__, url_prefix='/auth')


def validation_error(status_code, message):
    response = jsonify({
        'status': 'error',
        'message': message,
        'statusCode': status_code
    })
    response.status_code = status_code
    return response

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json
    required_fields = ['firstName', 'lastName', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return validation_error(422, f'{field} is required')
        
    if User.query.filter_by(email=data['email']).first():
        return validation_error(422, 'Email already exists')
    
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        userId = data['userId'],
        firstName = data['firstName'],
        lastName = data['lastName'],
        email = data['email'],
        password = hashed_password,
        phone = data.get('phone')
    )
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)

    return jsonify({
        'status': 'success',
        'message': 'Registration successful',
        'data': {
            'access_token': access_token,
            'user': {
                'userId': new_user.userId,
                'firstName': new_user.firstName,
                'lastName': new_user.lastName,
                'email': new_user.email,
                'phone': new_user.phone
            }
        }
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            return validation_error(422, f'{field} is required')
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return validation_error(401, 'Invalid email or password')
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'data': {
            'access_token': access_token,
            'user': {
                'userId': user.userId,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'phone': user.phone
            }
        }
    }), 200