import requests
import time
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup


class GoodReadsScraper():
    """ This module scraps the infromation from the Goodreads webpage.
    You provide list of ISBN's as the argument and then magic happens.

    attributes obtained: author, title, number of pages, edition, cover_url, genres
    """
    
    def __init__(self, isbns):
        self.isbns = isbns
        self.soups = [BeautifulSoup(requests.get(f'https://www.goodreads.com/book/isbn/{i}').text, 'html.parser') for i in self.isbns]


    def __str__(self):
        return f"So you plan to scrap data for {len(self.isbns)} books from the Goodreads.com?"

    def _goodreads_scraping(self):
        """ this method extracts number of pages, book's edition
        and cover picture url from accrued html texts.
        
        """
        isbn_13, pages, edition, cover_pic_url = [], [], [], []
        for s, i in zip(self.soups, self.isbns):
            isbn_13.append(i)
            pages.append(getattr(s.find(itemprop="numberOfPages"), 'text', None))
            edition.append(getattr(s.find(itemprop="bookFormat"), 'text', None))
            cover = s.find(id='coverImage')['src']
            if cover is not None:
                cover_pic_url.append(cover)
        return isbn_13, pages, edition, cover_pic_url
            

    def data_converter(self):
        # convertes previously extracted list into dataframe
        i, p, e, c = self._goodreads_scraping()
        df = pd.DataFrame({'isbn13': i,
                            'pages': p,
                            'edition': e,
                            'cover_pic_url': c})
        return df


    def _genre_scraping(self):
        """ 
        This method extracts three top genres of the book.

        """
        isbn_13, g1, g2, g3 = [], [], [], []
        for s, i in zip(self.soups, self.isbns):
            isbn_13.append(i)
            genrs = s.find_all(class_='actionLinkLite bookPageGenreLink')[0:3]
            g1.append(getattr(genrs[0], 'text', None))
            g2.append(getattr(genrs[1], 'text', None))
            g3.append(getattr(genrs[2], 'text', None))
        return isbn_13, g2, g2, g3
            

    def genre_converter(self):
        # convertes previously extracted list into dataframe
        i, g1, g2, g3 = self._genre_scraping()
        df = pd.DataFrame({'isbn13': i,
                        'primary_genre': g1,
                        'secondary_genre': g2,
                        'tertiery_genre': g3})
        return df
    
    
    def _meta_scraping(self):
        """ This method extracts meta data of the book.
        Book's title and author's full name.
        
        """
        isbn_13, author, title = [], [], []
        for s, i in zip(self.soups, self.isbns):
            isbn_13.append(i)
            author.append(getattr(s.find(class_='authorName'), 'text', None))
            title.append(getattr(s.find(class_="gr-h1 gr-h1--serif"), 'text', None))
        return isbn_13, author, title


    def meta_converter(self):
        # convertes previously extracted list into dataframe
        i, a, t = self._meta_scraping()
        df = pd.DataFrame({'isbn13': i,
                        'author': a,
                        'title': t})
        return df
