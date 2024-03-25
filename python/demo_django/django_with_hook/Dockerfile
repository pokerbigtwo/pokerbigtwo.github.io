# Dockerfile
FROM python:3.10.11
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install django
COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["python","test_django/manage.py","runserver","0.0.0.0:5000"]