from django import forms
from .models import *


class BookForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    if args.__len__() < 1:
      super(BookForm, self).__init__(*args, **kwargs)
      return
    context = args[0]
    right_context = {
      'title': context['title'],
      'author': context['author'],
      'category': Category.objects.get(name=context['category'])
    }
    new_args = [right_context, *args[1:]]
    super(BookForm, self).__init__(*new_args, **kwargs)

  class Meta:
    model = Book
    fields = ['title', 'author', 'category']


class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['name']
