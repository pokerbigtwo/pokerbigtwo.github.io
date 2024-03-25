# Dockerfile
FROM python:3.10.11
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install bottle
COPY . /app
EXPOSE 9453
CMD ["python","eof_2021_ssrf_with_hook.py"]