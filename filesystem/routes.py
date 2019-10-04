import sys
from flask import request, Blueprint, make_response
import os
import json
from helpers.s3_client import upload_file_to_s3

file_system_blueprint = Blueprint("file_system_blueprint", __name__)


@file_system_blueprint.route("", methods=["POST"])
def file_upload():
    # data = request.stream.readlines()
    file = request.files["file"]
    upload_file_to_s3(file, "easymlfiles")
    return make_response(json.dumps({"message": "Upload successful"}), 200)


@file_system_blueprint.route("/dataset", methods=["GET"])
def dataset():
    if request.method == "GET":
        # files = request.
        path = os.path.abspath(sys.modules['__main__'].__file__)[:-14] + "uploads"
        return str(os.listdir(path))