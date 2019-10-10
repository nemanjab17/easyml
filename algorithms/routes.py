from flask import request, Blueprint, make_response
import json
from config import logistic_regression
import inject
from algorithms.sklearnWrapper import SklearnWrapper
algorithms = Blueprint('algorithms', __name__)


@algorithms.route('/', methods=["GET"])
def algorithms():
    if request.method == "GET":
        algorithm_list = ["Logistic Regression", "Naive Bayes", "Decision Tree", "Random Forrest Classifier"]
        return make_response(json.dumps({"algorithms": algorithm_list}), 200)


@algorithms.route('/{alg}/parameters',  methods=["GET"])
def get_alg_parameters(alg):
    pass
    #citaj iz nekog dicta parametre za svaki model
    alglist = {"Logistic Regression": logistic_regression,
               "Naive Bayes": [],
               "Decision Tree": [],
               "Random Forrest Classifier": []}
    return make_response(json.dumps({str(alg): alglist[alg]}), 200)


@algorithms.route("/runner", methods=["POST"])
def mlrun():
    alg = request.body.get("algorithm")
    param = inject.instance(alg)(request.body.get("parameters"))
    wrapper = SklearnWrapper(alg,param)
    return make_response(json.dumps({"message": "succesful run!"}), 200)
