ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY . /code
RUN pip3 install .

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "mysite.wsgi"]
