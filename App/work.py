from functools import lru_cache

import numpy as np
import pandas as pd

from .const import *
from .models import Category, Book

pd.set_option('display.max_columns', None)


# @lambda _:_()
@lru_cache(None)
def get_example_books() -> list[dict]:
  # print(os.system('dir'))
  # https://www.kaggle.com/datasets/egehanyorulmaz/books-with-author-and-title-by-language-levels
  frame = pd.read_csv('book_levels.csv')
  frame = frame.dropna().drop_duplicates()
  frame: pd.DataFrame = frame.rename(columns={'Title': 'title', 'Author': 'author', 'Language Level': 'category'})

  date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
  date_range = date_range.strftime('%Y-%m-%d %H:%M:%S').to_numpy()[:frame.__len__()]
  np.random.shuffle(date_range)
  # print(date_range)
  frame['date_added'] = date_range
  np.random.shuffle(date_range)
  frame['date_updated'] = date_range
  # print(frame.to_dict(orient='records'))
  return frame.to_dict(orient='records')


def books2ORM():
  array = []
  for book in get_example_books():
    book = book.copy()
    book['category'] = Category.objects.get_or_create(name=book['category'])[0]
    array.append(Book(**book))
  Book.objects.bulk_create(array)


def get_filtered_books(category, search):
  books = Book.objects.filter(category=category)
  return list(filter(lambda x: search.lower() in x.title.lower() or search.lower() in x.author.lower(), books))


def get_categories_and_books(page: int, sort_by: str, search: str) -> list[dict]:
  page = max(0, int(page))
  if sort_by not in sort_by_list:
    sort_by = 'title'

  # category_books = [
  #   [
  #     [
  #       book.title, book.author, book.category, book.date_added, book.date_updated, book.id
  #     ]
  #     for book in Book.objects.filter(category=category)
  #   ]
  #   for category in Category.objects.all()
  # ]
  # category_books = [pd.DataFrame(cb, columns=books_columns_with_id) for cb in category_books]
  # category_books = pd.concat(category_books)
  # print(list(Book.objects.filter()))
  category_books = [
    [
      book.title, book.author, book.category,
      book.date_added.strftime('%Y-%m-%d %H:%M:%S'),
      book.date_updated.strftime('%Y-%m-%d %H:%M:%S'),
      book.id
    ]
    for book in Book.objects.filter()
  ]
  category_books = pd.DataFrame(category_books, columns=books_columns_with_id)
  category_books = category_books.astype(pdbookscast)
  filter_mask = category_books['title'].str.contains(search, case=False)
  filter_mask |= category_books['author'].str.contains(search, case=False)
  filter_mask |= category_books['category'].str.contains(search, case=False)
  is_in_date = category_books['date_added'].apply(lambda x: search in timeisoformat(x))
  filter_mask |= is_in_date

  category_books = category_books[filter_mask]
  category_books = category_books.sort_values(by=sort_by)
  category_books['date_added'] = category_books['date_added'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
  category_books['date_updated'] = category_books['date_updated'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
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
