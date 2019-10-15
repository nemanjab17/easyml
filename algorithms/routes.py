from flask import request, Blueprint, make_response
import json
from algorithms.alg_data import (
    logistic_regression,
    naive_bayes,
    rfc,
    decision_tree
    )
import inject
from algorithms.sklearnWrapper import SklearnWrapper
algorithms = Blueprint('algorithms', __name__)


@algorithms.route('', methods=["GET"])
def all_algorithms():
    if request.method == "GET":
        algorithm_list = ["Logistic Regression", "Naive Bayes", "Decision Tree", "Random Forrest Classifier"]
        return make_response(json.dumps({"algorithms": algorithm_list}), 200)


@algorithms.route('/<alg>/parameters',  methods=["GET"])
def get_alg_parameters(alg):
    alglist = {"Logistic Regression": logistic_regression,
               "Naive Bayes": naive_bayes,
               "Decision Tree": decision_tree,
               "Random Forrest Classifier": rfc
               }

    return make_response(json.dumps({str(alg): alglist[alg]}), 200)


@algorithms.route("/runner", methods=["POST"])
def mlrun():
    alg = request.body.get("algorithm")
    param = inject.instance(alg)(request.body.get("parameters"))
    wrapper = SklearnWrapper(alg, param)
    return make_response(json.dumps({"message": "succesful run!"}), 200)
