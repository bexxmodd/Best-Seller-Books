import requests
import time
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup


class GoodReadsScraper():
    """ This module will be used to scrap the infromation from the Goodreads webpage
    based on provided list of ISBN13 numbers.

    attributes obtained: author, title, number of pages, edition, cover_url, genres
    """
    lapse = 3

    def __init__(self, isbns):
        self.isbns = isbns

    def __str__(self):
        return f"So you plan to scrap data about {len(self.isbns)} books from the Goodreads.com?"
    
    @property
    def set_lapse(cls, seconds):
        cls.lapse = seconds


    def _goodreads_scraping(self):
        isbn_13, pages, edition, cover_pic_url = [], [], [], []

        for isbn in self.isbns:
            isbn_13.append(isbn)
            time.sleep(2)

            r = requests.get(f'https://www.goodreads.com/book/isbn/{isbn}')
            soup = BeautifulSoup(r.text, 'html.parser')

            pages.append(soup.find(itemprop="numberOfPages").text)
            edition.append(soup.find(itemprop="bookFormat").text)
            cover_pic_url.append(soup.find(id='coverImage')['src'])
            
        return isbn_13, pages, edition, cover_pic_url
            

    def data_converter(self):
        i, p, e, c = self._goodreads_scraping()
        df = pd.DataFrame({'isbn13': i,
                            'pages': p,
                            'edition': e,
                            'cover_pic_url': c})
        return df


    def _genre_scraping(self):
        isbn_13, g1, g2, g3 = [], [], [], []
        for isbn in self.isbns:
            isbn_13.append(isbn)
            time.sleep(2)

            r = requests.get(f'https://www.goodreads.com/book/isbn/{isbn}')
            soup = BeautifulSoup(r.text, 'html.parser')

            genrs = soup.find_all(class_='actionLinkLite bookPageGenreLink')[0:3]
            g1.append(genrs[0].text)
            g2.append(genrs[1].text)
            g3.append(genrs[2].text)
        return isbn_13, g2, g2, g3
            

    def genre_converter(self):
        i, g1, g2, g3 = self._genre_scraping()
        df = pd.DataFrame({'isbn13': i,
                        'primary_genre': g1,
                        'secondary_genre': g2,
                        'tertiery_genre': g3})
        return df
    
    
    def _meta_scraping(self):
        isbn, author, title = [], [], []
        for isbn in self.isbns:
            isbn_13.append(isbn)
            time.sleep(2)

            r = requests.get(f'https://www.goodreads.com/book/isbn/{isbn}')
            soup = BeautifulSoup(r.text, 'html.parser')
            author.append(soup.find(class_='authorName').text)
            title.append(soup.find(class_="gr-h1 gr-h1--serif").text)
        return isbn, author, title


    def meta_converter(self):
        i, a, t = self._meta_scraping()
        df = pd.DataFrame({'isbn13': i,
                        'author': g1,
                        'title': g2})
        return df