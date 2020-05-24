import pandas as pd
import requests
import json
import time

from tqdm import tqdm
from datetime import datetime


class TimesExtractor:
    """
    Purpose of this class is to extrac best seller books from the Times API.
    Times has limit on how many requests you can send, so we have to do with
    small ranges and then combine all the collected data into one dataframe.
    """

    # this is a default api-key which can be changed
    api_key = 'djDLXwAoSfreMrzYGE5iacl7GUifIRrV'

    def __init__(self, start_date, end_date, frq):
        self.start_date = start_date
        self.end_date = end_date
        self.frq = frq

    def __rep__(self):
        return f"The bestellers list is from {self.start_date} to {self.end_date}"

    def _datesrange(self):
        """ Enter dates in 'yyyy-mm-dd' format.
        For f -> 'D'=day; 'W'=week; 'M'=month; 'Y'=year. """
        return pd.date_range(start=self.start_date, end=self.end_date, freq=self.frq)

    @classmethod
    def key(cls, key):
        cls.api_key = key

    def extractor(self):
        """
        This function iterats throug the dates and sends the request
        to the Times API based on given set of dates. After that combines
        all the extracted dictionaries and returns as a combined dictionary.
        """
        super_dict = {}
        for date in tqdm(self._datesrange()):
            """ API has a limit how many calls you make
            per mnt. We set up the lapses between calls """
            time.sleep(3)
            print(date)
            res = requests.get("https://api.nytimes.com/svc/books/v3/lists/{date}/combined-print-and-e-book-fiction.json?",
                            params = {'api-key': self.api_key}).json()
            super_dict.update(res)
        return super_dict
