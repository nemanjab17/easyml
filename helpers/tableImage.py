import pandas as pd
class TableImage:

    def __init__(self, table_name, type=None):
        self.type = "csv" if type is None else type
        self.table_name = table_name
        self.folder = "../uploads"
        self.abs_path = self.folder + "/"+self.table_name +"."+self.type



    def get_table_columns(self):
        df = pd.read_csv(self.abs_path)
        return list(df.columns.values)

    def is_bad_file(self):
        try:
            df = pd.read_csv(self.abs_path)
            return False
        except FileNotFoundError:
            return True

    def get_header(self):
        return pd.read_csv(self.abs_path).head().to_dict()



