logistic_regression = [
    ("penalty", "string", "str, ‘l1’, ‘l2’, ‘elasticnet’ or ‘none’, optional (default=’l2’)"),
    ("C", "float", "float, optional (default=1.0)"),
    ("solver", "string", "str, {‘newton-cg’, ‘lbfgs’, ‘liblinear’, ‘sag’, ‘saga’}, optional (default=’liblinear’)"),
    ("max_iter", "int", "int, optional (default=100)")
]
naive_bayes = []
decision_tree = [
    ("criterion", "string", "string, optional (default='gini')"),
    ("max_depth", "int", "int or None, optional (default=None)"),
    ("max_features", "int", "int or  None, optional (default=None)"),
    ("max_leaf_nodes", "int", "int or None, optional (default=None)")
]

rfc = [
    ("criterion", "string", "string, optional (default='gini')"),
    ("max_depth", "int", "int or None, optional (default=None)"),
    ("max_features", "int", "int or  None, optional (default=None)"),
    ("max_leaf_nodes", "int", "int or None, optional (default=None)")
]