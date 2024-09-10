import os.path

import pandas as pd
from django.test import TransactionTestCase

from App.models import Book, Category
from App.work import get_categories_and_books



class TestWork(TransactionTestCase):
  def setUp(self):
    books2ORM()
  def test_get_categories_and_books(self):
    res1 = get_categories_and_books(1, 'title', 'a')
    print(res1)
