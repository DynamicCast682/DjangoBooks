import datetime

import pandas as pd
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from App.const import sort_by_list
from App.forms import BookForm, CategoryForm
from App.models import *
from App.work import get_categories_and_books, books2ORM


# Create your views here.


def test(request):
  return render(request, 'test.html')


def index(request):
  if request.method != 'GET':
    return render(request, '404.html')
  search = request.GET.get('search', '')
  page = request.GET.get('page', 1)
  sort_by = request.GET.get('sort_by', 'title')
  page = max(0, int(page))
  if sort_by not in sort_by_list:
    sort_by = 'title'

  context = {
    "page": page,
    "lpn": max(0, page - 1),
    "rpn": page + 1,
    "category_books": get_categories_and_books(page, sort_by, search),
    'sort_by': sort_by,
    'sort_by_list': sort_by_list,
    'search': search
  }

  return render(request, 'index.html', context=context)


class BookActions:
  @classmethod
  def add(cls, request):
    if request.method == 'POST':
      form = BookForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('/books/')
    else:
      form = BookForm()
    return render(request, 'add_book.html', {
      'form': form,
      'categories': Category.objects.all()
    })

  @classmethod
  def edit(cls, request):
    if request.method == 'POST':
      book = Book.objects.get(id=request.POST['book_id'])
      form = BookForm(request.POST, instance=book)
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

  @classmethod
  def delete(cls, request):
    if request.method == 'GET':
      book = Book.objects.get(id=request.GET['book_id'])
      book.delete()
    return redirect('/books/')


class CategoryActions:

  @classmethod
  def add(cls, request):
    if request.method == 'POST':
      form = CategoryForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('/books/add_category/')
    else:
      form = CategoryForm()
    return render(request, 'add_category.html', {
      'form': form,
      'categories': Category.objects.all()
    })

  @classmethod
  def edit(cls, request):
    if request.method == 'POST':
      category = Category.objects.get(id=request.POST['category_id'])
      form = CategoryForm(request.POST, instance=category)
      if form.is_valid():
        form.save()
        return redirect('/books/add_category/')
    else:
      category = Category.objects.get(id=request.GET['category_id'])
      form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {
      'form': form,
      'category': category,
      'categories': Category.objects.all()
    })

  @classmethod
  def delete(cls, request):
    if request.method == 'POST':
      category = Category.objects.get(id=request.POST['category_id'])
      category.delete()
    return redirect('/books/add_category/')


def random_fill(request):
  Book.objects.all().delete()
  Category.objects.all().delete()
  books2ORM()
  return redirect('/books/')
