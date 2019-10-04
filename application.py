from flask import Flask, make_response, jsonify
from filesystem.routes import file_system_blueprint
from algorithms.routes import algorithms
from auth.routes import auth_blueprint
from resources.test import test_blueprint
import inject
from algorithms.base_interface import LogisticInterface
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from database.db import DB_URI
from easyml_util.exceptions import EasyMLExceptions

engine = create_engine(DB_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def config(binder):
    binder.bind("Logistic Regression", LogisticInterface)
    binder.bind("dbsession", db_session)
    binder.bind("jwt_secret", "secret")


inject.configure(config)

application = Flask(__name__)


@application.errorhandler(EasyMLExceptions)
def error_handler(error):
    return make_response(jsonify({
        "message": error.message
    })), error.code


application.register_blueprint(file_system_blueprint, url_prefix='/files')
application.register_blueprint(algorithms, url_prefix='/algorithm')
application.register_blueprint(test_blueprint, url_prefix='/test')
application.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    application.run(debug=True)




