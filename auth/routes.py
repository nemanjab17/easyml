from flask import request, Blueprint, make_response, jsonify
from auth.manager import DatabaseManager
from auth.jwt_functions import encode_auth_token
from auth.validation import UserLoginValidation
auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/login', methods=["POST"])
def login():
    post_data = request.get_json()
    UserLoginValidation(post_data).validate_and_raise()
    db = DatabaseManager()
    user = db.get_user_by_email(post_data.get("email"))
    if not user:
        return make_response(jsonify(
            {"message": "No user registered with that email."})), 404
    if user.password != post_data.get("password"):
        return make_response(jsonify(
            {"message": "Wrong email and/or password!"})), 404
    token = encode_auth_token(user.id)
    resp = make_response(jsonify({"message": "Log in successful!"}))
    resp.set_cookie("user", token)
    return resp, 200


@auth_blueprint.route('/register', methods=["POST"])
def register():
    post_data = request.get_json()
    db = DatabaseManager()
    user = db.get_user_by_email(post_data.get("email"))
    if not user:
        db.add_user(post_data)
        return make_response(jsonify({"message": "Registration Successful!"})), 201
    else:
        response_object = {
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(response_object)), 202


@auth_blueprint.route('/logout', methods=["GET"])
def logout():
    resp = make_response(jsonify({"message": "Log out successful!"}))
    resp.set_cookie("user", "")
    return resp, 200

