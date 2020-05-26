import pandas as pd
import requests
import json
import time
import re

from tqdm import tqdm
from datetime import datetime


class TimesExtractor:
    """ The purpose of the module is to extract books data from the Times API.

    Times has a limit on how many requests you can send, so we have to do
    with time lapses and then combine all the collected data into one list.

    """

    # Default api-key which can be changed.
    api_key = 'djDLXwAoSfreMrzYGE5iacl7GUifIRrV'

    # Default lapse between calls
    lapse = 3

    def __init__(self, start_date, end_date, frq):
        """ Please enter dates in 'yyyy-mm-dd' format.

        For frq -> 'D'=day; 'W'=week; 'M'=month; 'Y'=year.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.frq = frq

        # Raise Error if entered value doesn't match the pattern.
        if not re.search(r"^\d{4}-\d{2}-\d{2}$", self.start_date):
            raise ValueError('please enter start_date in \'yyyy-mm-dd\' format')
        elif not re.search(r"^\d{4}-\d{2}-\d{2}$", self.end_date):
            raise ValueError('please enter end_date in \'yyyy-mm-dd\' format')
        elif self.frq not in ('D', 'W', 'M', 'Y'):
            raise ValueError('please enter frequency in correct format')
        else:
            pass


    def __str__(self):
        return f"The bestellers list is from {self.start_date} to {self.end_date}"

    def _datesrange(self):
        if self.start_date >= self.end_date:
            return [self.end_date]
        else:
            dates = [d for d in pd.date_range(start=self.start_date,
                                        end=self.end_date,
                                        freq=self.frq).strftime('%Y-%m-%d')]
            return dates


    @classmethod
    def key(cls, key):
        cls.api_key = key

    @classmethod
    def seconds(cls, second):
        cls.lapse = second


    def make_call(self):
        """ This function iterates through the dates and sends the request
        to the Times API for the given set of dates.
        
        Next, it returns all the dictionaries as a combined list.
        """

        super_list = []
        print(f'Due to API\'s limitation, there is a {self.lapse} second lapse between calls')
        for date in tqdm(self._datesrange()):
            """ Times API has a daily limit on calls
            and a requirement for intervals between calls.
            
            Thus, we set up the lapses between calls.
            """

            time.sleep(self.lapse)
            print(date)
            res = requests.get(f"https://api.nytimes.com/svc/books/v3/lists/{date}/combined-print-and-e-book-fiction.json?",
                                params = {'api-key': self.api_key}).json()
            super_list.append(res['results']['books'])
        return super_list