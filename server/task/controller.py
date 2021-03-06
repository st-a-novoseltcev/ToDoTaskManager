from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

from server import BaseConfig
from server.errors.exc import InvalidSchema
from server.jwt_auth import admin_required
from server.task import service as task_service
from server.task.service import TaskSchema


task_blueprint = Blueprint('task', __name__)


@task_blueprint.route('/task/', methods=['POST'])
@jwt_required()
def create():
    id_user = get_jwt_identity()
    try:
        schema = TaskSchema(only=('title', 'id_category')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    id = task_service.create(id_user, schema)
    schema['id'] = id
    return jsonify(schema), 201


@task_blueprint.route('/task/', methods=['PUT'])
@jwt_required()
def edit():
    id_user = get_jwt_identity()
    try:
        schema = TaskSchema().load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    task_service.update(id_user, schema)
    return jsonify(schema), 202


@task_blueprint.route('/task/', methods=['DELETE'])
@jwt_required()
def delete():
    id_user = get_jwt_identity()
    try:
        id = TaskSchema(only=('id',)).load(request.json)['id']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    response = task_service.delete(id_user, id)
    return jsonify(response), 202


@task_blueprint.route('/admin/task/', methods=['DELETE'])
@admin_required(BaseConfig.admin_roles)
def delete_4_admin():
    try:
        schema = TaskSchema(only=('id', 'id_user')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    response = task_service.delete(**schema)
    return jsonify(response), 202
