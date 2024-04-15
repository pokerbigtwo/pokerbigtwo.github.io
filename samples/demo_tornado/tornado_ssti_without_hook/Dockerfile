# Dockerfile
FROM python:3.10.11
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install tornado
COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["python","server.py"]