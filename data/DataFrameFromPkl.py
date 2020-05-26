import pandas as pd

class DataFrameFromPkl(object):
    """
    Temporarily imports data frame columns and deletes them afterwards.
    """

    def __init__(self, pickle):
        self.df = pd.read_pkl(pickle)
        self.columns = list(self.df.columns.values)

    def __enter__(self):
        return self.df

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.df.drop([c for c in self.columns], axis=1, inplace=True)

