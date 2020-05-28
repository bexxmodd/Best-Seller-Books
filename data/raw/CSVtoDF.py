import pandas as pd

class CSVtoDF(object):
    """
    Temporarily imports data frame columns from .csv file
    and deletes them after selecting the needed columns.

    """

    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.columns = list(self.df.columns.values)

    def __enter__(self):
        return self.df

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.df.drop([c for c in self.columns], axis=1, inplace=True)

