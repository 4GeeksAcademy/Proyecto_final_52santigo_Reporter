from flask import Blueprint, request, jsonify, abort
from app.models.user_model import User
from app.services.task_service import create_task

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('/<int:user_id>', methods=['POST'])
def add_task(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, 'Usuario no encontrado')

    data = request.get_json()
    task = create_task(data, user)
    return jsonify(task.to_dict()), 201
