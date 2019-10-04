from flask import request, Blueprint, make_response
dataset_blueprint = Blueprint("table_blueprint", __name__)
import os
import sys
import requests

@dataset_blueprint.route("", methods=["GET"])
def dataset():
    if request.method == "GET":
        #files = request.
        path = os.path.abspath(sys.modules['__main__'].__file__)[:-14] + "uploads"
        return str(os.listdir(path))


