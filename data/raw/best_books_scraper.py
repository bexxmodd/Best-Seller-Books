import numpy as np
import requests

from bs4 import BeautifulSoup


class BestBooks():

    def __init__(self, pages):
        self.pages = pages
        self.soups = [BeautifulSoup(requests.get(f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={n}').text,
                                                                        'html.parser') for n in range(1, self.pages + 1)]

    def __str__(self):
        return f"You just scraped {self.pages} pages from the GoodReads.com!"
    
    def store_html(self):
        # If you want to store scraped HTML as a list
        return self.soups

    def books_authors(self):
        titles, authors = [], []
        for page in self.soups:
            for title, author in zip(page.find_all(class_="bookTitle"), page.find_all(class_="authorName")):
                titles.append(title.get_text())
                authors.append(author.get_text())
        return [titles, authors]

s = BestBooks(1)
print(s.books_authors())