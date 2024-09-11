from functools import lru_cache

import numpy as np
import pandas as pd

from .models import Category, Book

pd.set_option('display.max_columns', None)


# @lambda _:_()
def get_example_books() -> list[dict]:
  # print(os.system('dir'))
  # https://www.kaggle.com/datasets/egehanyorulmaz/books-with-author-and-title-by-language-levels
  frame = pd.read_csv('book_levels.csv')
  frame = frame.dropna().drop_duplicates()
  frame: pd.DataFrame = frame.rename(columns={'Title': 'title', 'Author': 'author', 'Language Level': 'category'})
  return frame.to_dict(orient='records')


def books2ORM():
  array = []
  for book in get_example_books():
    book['category'] = Category.objects.get_or_create(name=book['category'])[0]
    array.append(Book(**book))
  Book.objects.bulk_create(array)


def get_filtered_books(category, search):
  books = Book.objects.filter(category=category)
  return list(filter(lambda x: search.lower() in x.title.lower() or search.lower() in x.author.lower(), books))


def get_categories_and_books(page: int, sort_by: str, search: str) -> list[dict]:
  columns = ['name', 'title', 'author', 'id']
  category_books = [
    [
      [
        category.name, book.title, book.author, book.id
      ]
      for book in Book.objects.filter(category=category)
    ]
    for category in Category.objects.all()
  ]
  category_books = [pd.DataFrame(cb, columns=columns) for cb in category_books]
  category_books = pd.concat(category_books)
  filter_mask = category_books['title'].str.contains(search, case=False)
  filter_mask |= category_books['author'].str.contains(search, case=False)
  filter_mask |= category_books['name'].str.contains(search, case=False)

  category_books = category_books[filter_mask]
  category_books = category_books.sort_values(by=sort_by).reset_index(drop=True)
  step = 10
  category_books = category_books.iloc[step * (page - 1):step * page]
  # gbd = category_books.groupby('name')
  # result = []
  # for gb in gbd.groups:
  #   name = gb
  #   group = gbd.get_group(gb).sort_values(by=sort_by)
  #   result.append({
  #     'name': name,
  #     'books': group[['title', 'author', 'id']].to_dict(orient='records')
  #   })
  return category_books.to_dict(orient='records')
