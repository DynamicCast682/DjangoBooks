import datetime

import pandas as pd

sort_by_list = ['title', 'author', 'category', 'date_added', 'date_updated']
books_columns = sort_by_list
books_columns_with_id = books_columns.copy() + ['id']
pdbookscast = {
  'title': 'string',
  'author': 'string',
  'category': 'string',
  'date_added': 'datetime64[ns]',
  'date_updated': 'datetime64[ns]',
}

def timecast(time_string: str) -> datetime.datetime:
  return datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')


def timeisoformat(this_time: datetime.datetime | str) -> str:
  if type(this_time) is datetime.datetime:
    time_string = this_time.isoformat(sep=' ').split('+')[0]
    time_string = time_string.split('.')[0]
    return time_string
  elif type(this_time) is pd.Timestamp:
    return this_time.isoformat()

  return this_time