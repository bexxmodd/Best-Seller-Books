from pandas import json_normalize

class DataFrameFromDict(object):
    """
    Temporarily imports data frame columns and deletes them afterwards.
    """

    def __init__(self, data):
        self.df = json_normalize(data)
        self.columns = list(self.df.columns.values)

    def __enter__(self):
        return self.df

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.df.drop([c for c in self.columns], axis=1, inplace=True)