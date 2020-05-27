import requests
import time
import pandas as pd
import numpy as np

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


if __name__ == "__main__":
    print('This method is intended to be used within Jupyter Notebook...')