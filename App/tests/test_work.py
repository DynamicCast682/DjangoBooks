import json
import os.path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from django.test import Client, TransactionTestCase, TestCase, LiveServerTestCase
from django.urls import reverse

from App.const import *
from App.models import Book, Category
from App import work
from App.work import get_example_books, get_categories_and_books


ISCI = os.environ.get('ISCI', 'false') == 'true'

class TestWork(LiveServerTestCase):
  def setUp(self):
    self.client = Client()
    work.books2ORM()
    self.exemple_books = pd.DataFrame(get_example_books())

  def test_exemple_books_id_dataframe(self):
    self.assertIs(type(self.exemple_books), pd.DataFrame)
    print(self.exemple_books)
    # python manage.py test App.tests.test_work.TestWork.test_exemple_books_id_dataframe

  def test_ci_cd(self):
    self.assertEqual(1, 1)

  def test_index_html(self):
    # func_res: list[dict] = get_categories_and_books(1, 'title', 'a')
    for page in range(1, 4):
      for sort_by in sort_by_list:
        optional_data = {
          'sort_by': sort_by,
          'page': page,
        }
        print(f'{sort_by=}')
        response = self.client.get(reverse('main_page'), data=optional_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
        all_tr = soup.select(f'tbody > tr')
        table = []
        for tr in all_tr:
          setr: list = tr.select(f'td')

          table.append([*[item.text for item in setr[:3]], timecast(setr[3].text), timecast(setr[4].text)])
        front_books_frame = pd.DataFrame(table, columns=books_columns)
        front_books_frame = front_books_frame.astype(pdbookscast)
        self.assertEqual(front_books_frame.shape.__len__(), 2)
        right_front_books_frame = front_books_frame.copy().sort_values(by=optional_data['sort_by'])
        # print(front_books_frame['title'].dtype)
        front_books_frame = front_books_frame.to_numpy()
        right_front_books_frame = right_front_books_frame.to_numpy()

        self.assertEqual(front_books_frame.dtype, right_front_books_frame.dtype)
        front_right_assert = front_books_frame == right_front_books_frame
        error_where = np.where(~(front_right_assert))
        error_msg = f'''
        {sort_by=}\n
        {error_where}\n
        {front_books_frame}\n
        {right_front_books_frame}\n'''
        self.assertTrue(np.all(front_right_assert),
                        msg=error_msg)


    # python manage.py test App.tests.test_work.TestWork.test_index_html

  # python manage.py test App.tests.test_work.TestWork.

