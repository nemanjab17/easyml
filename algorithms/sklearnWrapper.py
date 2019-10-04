from helpers.tableImage import TableImage


class sklearnwrapper:
    """"""

    def __init__(self, metadata):
        """Constructor for sklearnwrapper"""
        self.columntypes = metadata['columntypes']
        self.datasetname = metadata['datasetname']
        self.algname = metadata['algname']
        self.algparams = metadata['algparams']
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
