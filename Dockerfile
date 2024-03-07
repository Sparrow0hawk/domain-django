FROM python:3.12-slim

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE="mysite.settings"

WORKDIR /app
COPY . /app

RUN pip3 install .

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 mysite.wsgi"]
