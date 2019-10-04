import json
from config import logistic_regression


class BaseInterface:

    def to_dict(self):
        item = {}
        for i in self.arglist:
            item[i] = self.__getattribute__(i)
        return item


class LogisticInterface(BaseInterface):

    def __init__(self, args):
        super().__init__()
        self.arglist = logistic_regression
        args = json.loads(args)
        self.penalty = args.get("penalty") if args.get("penalty") else "l2"
        self.c = args.get("C") if args.get("C") else 1.0
        self.solver = args.get("solver") if args.get("solver") else "liblinear"
        self.maxiter = args.get("maxiter") if args.get("maxiter") else 100




