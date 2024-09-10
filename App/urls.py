
from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index),
  path('test/', views.test),
  path('add_book/', views.add_book),
  path('add_category/', views.add_category),
  path('delete_book', views.delete_book),
  path('delete_category', views.delete_category),
  path('edit_book', views.edit_book),
  # path('')
]