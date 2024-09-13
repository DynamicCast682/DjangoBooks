

FROM python:3.11.9

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py", "test"]