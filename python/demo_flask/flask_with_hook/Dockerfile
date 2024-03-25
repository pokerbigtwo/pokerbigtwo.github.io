# Dockerfile
FROM python:3.10.11
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install flask
COPY . /app
ENV FLASK_APP=app
CMD ["python","app.py"]