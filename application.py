from flask import Flask, make_response, jsonify
application = Flask(__name__)
PORT = 5000
DEBUG = True

# import routes for different modules
from filesystem.routes import file_system_blueprint
from algorithms.routes import algorithms
from auth.routes import auth_blueprint


application.register_blueprint(file_system_blueprint, url_prefix='/files')
application.register_blueprint(algorithms, url_prefix='/algorithms')
application.register_blueprint(auth_blueprint, url_prefix='/auth')

application.config['TRAP_HTTP_EXCEPTIONS']=True

application.config['UPLOAD_FOLDER'] = "/Users/nemanja/Documents/Deve/easyml/uploads"

# initialize database and prepare session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database.db import DB_URI

engine = create_engine(DB_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))



from alembic.config import Config
from alembic import command
alembic_cfg = Config("database/alembic.ini")
command.stamp(alembic_cfg, "head")

# inject dependencies
import inject
from algorithms.base_interface import LogisticInterface


def config(binder):
    binder.bind("Logistic Regression", LogisticInterface)
    binder.bind("dbsession", db_session)
    binder.bind("jwt_secret", "secret")


inject.configure(config)

# register common exception handler in flask middleware
from easyml_util.exceptions import EasyMLExceptions


@application.errorhandler(EasyMLExceptions)
def error_handler(error):
    return make_response(jsonify({
        "message": error.message
    })), error.code

application.register_error_handler(Exception, error_handler)

@application.route("/", methods=["GET"])
def status_handler():
    return make_response(jsonify({
        "Application": "Easyml",
        "Running on port": PORT,
        "Status": "Running"
    })), 200


if __name__ == '__main__':
    application.run(debug=DEBUG, port=PORT, host="0.0.0.0")
