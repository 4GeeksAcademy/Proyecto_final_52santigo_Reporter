from flask import Blueprint, request, jsonify, abort
from app.models.user_model import User
from app.schemas.user_schema import UserSchema
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    validated_data = UserSchema().load(data)
    user = User(**validated_data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
