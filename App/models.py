from django.db import models


class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.name


class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  date_added = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title
