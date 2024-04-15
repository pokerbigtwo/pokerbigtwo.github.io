# Dockerfile
FROM python:3.10.11
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install pyramid
RUN pip install mako
COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["python","app.py"]