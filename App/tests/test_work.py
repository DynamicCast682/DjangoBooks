import json
import os.path
import random
import socket
import time
import uuid

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
      books_elements = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr')
      key = books_elements[0].text
      books_elements[0].find_elements(By.CSS_SELECTOR, 'td > a')[0].click()
      self.assertNotIn(key, self.__get_books_keys())

      # python manage.py test App.tests.test_work.TestBooks.test_delete_books --liveserver=0.0.0.0:8081

  books_edit_count = 4

  def test_edit_books(self):
    self.main_page()
    for i in range(1, 4):
      books_elements = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr')
      books_elements[0].find_elements(By.CSS_SELECTOR, 'td > a')[1].click()
      time.sleep(0.5)
      title_element = driver.find_element(By.ID, 'title')
      old_title = title_element.get_attribute('value')
      title_element.clear()
      new_title = f'{uuid.uuid4()}'
      title_element.send_keys(new_title)

      author_element = driver.find_element(By.ID, 'author')
      old_author = author_element.get_attribute('value')
      author_element.clear()
      new_author = f'{uuid.uuid4()}'
      author_element.send_keys(new_author)

      category_element = driver.find_element(By.ID, 'category')
      category_options = category_element.find_elements(By.TAG_NAME, 'option')
      ca_l = category_options.__len__()
      old_category = category_options[0].text
      for option in category_options:
        if option.get_attribute('selected') is not None:
          old_category = option.text
          break
      random_category = random.randint(0, ca_l - 1)
      new_category = category_options[random_category].text
      category_element.click()
      category_options[random_category].click()


      submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
      submit_button.click()
      time.sleep(1)

      # key = f'{new_title} {new_author} {new_category}'
      new_in_db = Book.objects.filter(title=new_title, author=new_author,
                                      category=Category.objects.get(name=new_category)).first()
      old_in_db = Book.objects.filter(title=old_title, author=old_author,
                                      category=Category.objects.get(name=old_category)).first()
      self.assertIsNotNone(new_in_db)
      self.assertIsNone(old_in_db)

    # python manage.py test App.tests.test_work.TestBooks.test_edit_books


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
