from flask import Blueprint, make_response
import json
from auth.authorize import authorize
test_blueprint = Blueprint('test_blueprint', __name__)


@test_blueprint.route('', methods=["GET"])
@authorize
def algorithm():
    return make_response(json.dumps({"message": "hello worldddddd"}), 200)
