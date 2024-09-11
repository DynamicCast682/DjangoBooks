import datetime

import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from App.forms import BookForm, CategoryForm
from App.models import *
from App.work import get_categories_and_books, books2ORM


# Create your views here.
def timecast(time_string: str) -> datetime.datetime:
  return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')


def timeisoformat(this_time: datetime.datetime | str) -> str:
  if type(this_time) is datetime.datetime:
    time_string = this_time.isoformat(sep=' ').split('+')[0]
    time_string = time_string.split('.')[0]
    return time_string
  return this_time


def test(request):
  return render(request, 'test.html')


def index(request):
  if request.method != 'GET':
    return render(request, '404.html')
  search = request.GET.get('search', '')
  page = request.GET.get('page', 1)
  page = max(0, int(page))
  sort_by = request.GET.get('sort_by', 'title')
  if sort_by not in ['title', 'author']:
    sort_by = 'title'
  context = {
    "page": page,
    "lpn": max(0, page - 1),
    "rpn": page + 1,
    "category_books": get_categories_and_books(page, sort_by, search),
    'sort_by': sort_by,
  }

  return render(request, 'index.html', context=context)


def add_book(request):
  if request.method == 'POST':
    context = {
      "title": request.POST['title'],
      "author": request.POST['author'],
      "category": Category.objects.get(name=request.POST['category'])
    }
    # print(context)
    form = BookForm(context)
    if form.is_valid():
      form.save()
      return redirect('/books/')
  else:
    form = BookForm()
  return render(request, 'add_book.html', {
    'form': form,
    'categories': Category.objects.all()
  })


def delete_book(request):
  if request.method == 'GET':
    book = Book.objects.get(id=request.GET['book_id'])
    book.delete()
  return redirect('/books/')


def edit_book(request):

  if request.method == 'POST':
    book = Book.objects.get(id=request.POST['book_id'])
    right_context = {
      "title": request.POST['title'],
      "author": request.POST['author'],
      "category": Category.objects.get(name=request.POST['category'])
    }
    form = BookForm(right_context, instance=book)
    if form.is_valid():
      form.save()
      return redirect('/books/')
  else:
    book = Book.objects.get(id=request.GET['book_id'])
    form = BookForm(instance=book)
  return render(request, 'edit_book.html', {
    'form': form,
    'book': book,
    'categories': Category.objects.all()
  })


def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/books/')
  else:
    form = CategoryForm()
  return render(request, 'add_category.html', {
    'form': form,
    'categories': Category.objects.all()
  })


def delete_category(request):
  if request.method == 'GET':
    category = Category.objects.get(id=request.GET['category_id'])
    category.delete()
  return redirect('/books/')


def random_fill(request):
  Book.objects.all().delete()
  Category.objects.all().delete()
  books2ORM()
  return redirect('/books/')