from django.urls import path, include
from . import views
from .views import BookActions, CategoryActions

urlpatterns = [
  path('', views.index, name='main_page'),
  path('test/', views.test),

  path('add_book/', views.BookActions.add),
  path('edit_book', views.BookActions.edit),
  path('delete_book', views.BookActions.delete),

  path('add_category/', views.CategoryActions.add),
  path('edit_category', views.CategoryActions.edit),
  path('delete_category', views.CategoryActions.delete),

  path('random_fill', views.random_fill),
]
