import json
import os.path
import socket
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from django.test import Client, TransactionTestCase, TestCase, LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from App.const import *
from App.models import Book, Category
from App import work
from App.work import get_example_books, get_categories_and_books

ISCI = os.environ.get('ISCI', 'false') == 'true'

server = 'http://localhost:4444/wd/hub'
if ISCI:
  print(f'{ISCI=}')
  options = webdriver.ChromeOptions()
  driver = webdriver.Remote(command_executor=server, options=options)
else:
  driver = webdriver.Chrome()


class TestBooks(StaticLiveServerTestCase):
  @classmethod
  def setUpClass(cls):
    cls.host = socket.gethostbyname(socket.gethostname())
    super(TestBooks, cls).setUpClass()

  def setUp(self):
    work.books2ORM()

  def main_page(self):
    # driver.get('http://localhost:8000')
    driver.get(self.live_server_url)

  def test_selenium_ci_cd(self):

    self.main_page()
    # input()
    self.assertIn('Books', driver.title)

    # python manage.py test App.tests.test_work.TestBooks.test_selenium_ci_cd

  def __get_books_keys(self):
    return [item.text for item in driver.find_elements(By.CSS_SELECTOR, 'tbody > tr')]

  def test_delete_books(self):
    self.main_page()

    for _ in range(1, 4):
      books_element = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr')
      key = books_element[0].text
      books_element[0].find_elements(By.CSS_SELECTOR, 'td > a')[0].click()
      self.assertNotIn(key, self.__get_books_keys())

      # python manage.py test App.tests.test_work.TestBooks.test_delete_books --liveserver=0.0.0.0:8081

  books_edit_count = 4

  def test_edit_books(self):
    self.main_page()
    for i in range(1, 4):
      ...


class TestWork(StaticLiveServerTestCase):
  def setUp(self):
    self.client = Client()
    work.books2ORM()
    self.exemple_books = pd.DataFrame(get_example_books())

  def test_exemple_books_id_dataframe(self):
    self.assertIs(type(self.exemple_books), pd.DataFrame)
    self.exemple_books.__str__()
    # print(self.exemple_books)
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
