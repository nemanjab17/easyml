from helpers.tableImage import TableImage


class SklearnWrapper:

    def __init__(self, algorithm, parameters):
        self.column_types = metadata['columntypes']
        self.dataset_name = metadata['datasetname']
        self.alg_name = metadata['algname']
        self.alg_params = metadata['algparams']
        self.metrics = metadata['metrics']

    def run(self):
        timage = TableImage(self.datasetname)
        #za neki dat spisak kolona vrati dataset koji odgovara tom spisku kolona

        #pozovi sklearnalg

        #daj parametre algoritmu koji je vratio sklearnalg
        #izvedi cross val ili sta vec
        #vrati metrike koje su trazene

    def sklearnalg(self, name):
        pass
        #vraca algoritam koji treba popuniti sa parametrima
