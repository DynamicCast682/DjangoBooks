import json
import os.path

import pandas as pd
from django.test import Client, TransactionTestCase, TestCase, LiveServerTestCase
from django.urls import reverse

from App.models import Book, Category
from App.work import get_categories_and_books, books2ORM


class TestWork(LiveServerTestCase):
  def setUp(self):
    self.client = Client()
    books2ORM()

  def test_ci_cd(self):
    self.assertEqual(1, 1)

  # def test_index_html(self):
  #   # func_res: list[dict] = get_categories_and_books(1, 'title', 'a')
  #   response = self.client.get(reverse('main_page'))
  #   print(response.content.decode('utf-8'))
  #
  #   self.assertEqual(response.status_code, 200)
  #   self.assertTemplateUsed(response, 'index.html')
