import pandas as pd
from flask import request, Blueprint, make_response
from io import StringIO
import json
from helpers.s3_client import upload_file_to_s3
file_upload_blueprint = Blueprint("file_upload_blueprint", __name__)


@file_upload_blueprint.route("", methods=["POST"])
def fule_upload():
    #data = request.stream.readlines()
    file = request.files["file"]
    upload_file_to_s3(file, "easymlfiles")
    return make_response(json.dumps({"message": "Upload successful"}), 200)

