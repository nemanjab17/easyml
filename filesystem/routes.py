from flask import request, Blueprint, make_response, jsonify
import json
from filesystem.s3_client import FileManager
from auth.jwt_functions import decode_auth_token
from werkzeug.datastructures import FileStorage
from flask import current_app as app
import os
import pandas as pd
file_system_blueprint = Blueprint("file_system_blueprint", __name__)


@file_system_blueprint.route("", methods=["POST"])
def file_upload():
    file = request.files["file"]
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    header = list(pd.read_csv(path).columns.values)
    os.remove(path)
    token = decode_auth_token(request.cookies.get('user'))
    file_id = FileManager().save_file(file, token, header)
    return make_response(json.dumps({"id": file_id}), 200)


@file_system_blueprint.route("", methods=["GET"])
def get_files_of_user():
    token = decode_auth_token(request.cookies.get('user'))
    files = FileManager().get_files_of_user(token, ['id','filename', 'content_type'])
    return make_response(json.dumps({"files": files}))


@file_system_blueprint.route("/<uuid:file_id>", methods=["DELETE"])
def delete_file(file_id):
    FileManager().remove_file(file_id)
    return make_response(json.dumps({"message": "Success!"}))


@file_system_blueprint.route("/<uuid:file_id>/header", methods=["GET"])
def get_file(file_id):
    header = FileManager().get_file_header(str(file_id))
    return make_response(json.dumps({"header": header,
                                     "id": str(file_id)}))


@file_system_blueprint.route("/<uuid:file_id>/header", methods=["PUT"])
def map_file(file_id):
    header = FileManager().add_header_metadata(str(file_id), request.get_json())
    return make_response(json.dumps({"header": header,
                                     "id": str(file_id)}))
