import pandas as pd
import numpy as np
import pandas as pd
import requests
import json
import time
import re

from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup


class GoodReadsScraper():
    """ This module scraps the information from the Goodreads webpage.
    You provide a list of ISBN's as the argument and then magic happens.

    attributes obtained: author, title, number of pages, edition, cover_url, genres
    """
    
    def __init__(self, isbns):
        self.isbns = isbns
        # Iterates over the list of ISBNs
        # Gets HTMLs and stores as a list
        self.soups = [BeautifulSoup(requests.get(f'https://www.goodreads.com/book/isbn/{i}').text, 'html.parser') for i in self.isbns]

    def __str__(self):
        return f"You just scrapped {len(self.isbns)} books from the Goodreads.com!"

    def _goodreads_scraping(self):
        """ This method extracts the number of pages,
            book's edition from accrued HTML texts.
        
        """
        isbn_13, pages, edition = [], [], []
        for s, i in zip(self.soups, self.isbns):
            isbn_13.append(i)
            pages.append(getattr(s.find(itemprop="numberOfPages"), 'text', None))
            edition.append(getattr(s.find(itemprop="bookFormat"), 'text', None))
        return isbn_13, pages, edition
            
    def data_converter(self):
        # Convertes previously extracted list into dataframe.
        i, p, e = self._goodreads_scraping()
        df = pd.DataFrame({'isbn13': i,
                            'pages': p,
                            'edition': e})
        return df

    def _genre_scraping(self):
        """ 
        This method extracts top three genres of the book.

        """
        isbn_13, g = [], []
        for s, i in zip(self.soups, self.isbns):
            isbn_13.append(i)
            g.append(s.find_all(class_='actionLinkLite bookPageGenreLink')[:3])
        return isbn_13, g
            
    def genre_converter(self):
        # Convertes previously extracted list into dataframe.
        i, g = self._genre_scraping()
        df = pd.DataFrame({'isbn13': i, 'genres': g})
        return df
    
    def _meta_scraping(self):
        """ This method extracts the metadata of the book.
            That is book's title and author's full name.
        
        """
        isbn_13, author, title = [], [], []
        for s, i in zip(self.soups, self.isbns):
            isbn_13.append(i)
            author.append(getattr(s.find(class_='authorName'), 'text', None))
            title.append(getattr(s.find(class_="gr-h1 gr-h1--serif"), 'text', None))
        return isbn_13, author, title

    def meta_converter(self):
        # Convertes previously extracted list into dataframe.
        i, a, t = self._meta_scraping()
        df = pd.DataFrame({'isbn13': i,
                            'author': a,
                            'title': t})
        return df

    def _pop_scraping(self):
        """
        This method extracts a book's rating and a count.

        """
        isbn_13, rating, count = [], [], []
        for s, i in zip(self.soups, self.isbns):
            isbn_13.append(i)
            rating.append(getattr(s.find(itemprop="ratingValue"), 'text', None))
            count.append(getattr(s.find(itemprop="ratingCount"), 'text', None))
        return isbn_13, rating, count

    def pop_converter(self):
        # Convertes previously extracted list into dataframe.
        i, r, c = self._pop_scraping()
        df = pd.DataFrame({'isbn13': i,
                            'rating': r,
                            'count': c})
        return df

    def _cover_scraper(self):
        """ This method grabs cover picture URL.

        This portion of the text is a bit problematic
        so it's handled using a try-except function.
        """
        isbn_13, cover_url = [], []
        for s, i in zip(self.soups, self.isbns):
            isbn_13.append(i)
            try:
                cover_url.append(s.find(id='coverImage')['src'])
            except TypeError:
                cover_url.append(np.NaN)
        return isbn_13, cover_url

    def cover_url_converter(self):
        # Convertes previously extracted list into dataframe.
        i, cu = self._cover_scraper()
        df = pd.DataFrame({'isbn13': i,
                            'cover_url': cu})
        return df


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



if __name__ == "__main__":
    print('This method is intended to be used within Jupyter Notebook...')