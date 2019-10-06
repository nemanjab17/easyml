from flask import request, Blueprint, make_response, jsonify
import json
from filesystem.s3_client import FileManager
from auth.jwt_functions import decode_auth_token

file_system_blueprint = Blueprint("file_system_blueprint", __name__)


@file_system_blueprint.route("", methods=["POST"])
def file_upload():
    file = request.files["file"]
    token = decode_auth_token(request.cookies.get('user'))
    file_id = FileManager().save_file(file, token)
    return make_response(json.dumps({"id": file_id}), 200)


@file_system_blueprint.route("", methods=["GET"])
def get_files_of_user():
    token = decode_auth_token(request.cookies.get('user'))
    files = FileManager().get_files_of_user(token)
    return make_response(json.dumps({"files": files}))


@file_system_blueprint.route("/<uuid:file_id>", methods=["DELETE"])
def delete_file(file_id):
    FileManager().remove_file(file_id)
    return make_response(json.dumps({"message": "Success!"}))

