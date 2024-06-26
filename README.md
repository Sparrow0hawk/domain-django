[![CI](https://github.com/Sparrow0hawk/django-minimal/actions/workflows/ci.yml/badge.svg)](https://github.com/Sparrow0hawk/django-minimal/actions/workflows/ci.yml)
# Domain driven Django

A Django project following the polls example in the Django tutorial but exploring some basic ideas from
[Domain Driven Design](https://www.dddcommunity.org/book/evans_2003/) as well as exploring Django.

## Setup

To use this project you will need:
- Python 3.12
- Docker
- Node 21
- cURL (optional)

1. Create virtual environment
   ```bash
   python3.12 -m venv --prompt . .venv
   ```
2. Install project dependencies
   ```bash
   # activate virtual environment
   . .venv/bin/activate
   
   # install dependencies including dev dependencies
   pip install .[dev]
   
   # install playwright browsers
   playwright install
   ```
3. Run Django command to collect static assets
   ```bash
   .venv/bin/python manage.py collectstatic
   ```
4. Install NPM package
   ```bash
   npm install
   ```
5. Build web assets
   ```bash
   npm run build
   ```
6. Start Django app on http://127.0.0.1:8000
   ```bash
   python manage.py runserver
   ```
7. Use cURL to POST data to local app
   ```bash
   # post data
   chmod +x data/add-data.sh
   ./data/add-data.sh
   
   # clear data
   chmod +x data/clear-data.sh
   ./data/clear-data.sh   
   ```
8. Run tests
   ```bash
   make test
   ```
9. Run full build
   ```bash
   make verify
   ```

## Docker

You can also build and run the app using Docker.

1. Build the container
   ```bash
   docker build . -t mysite-minimal
   ```
2. Run the app and view it at http://127.0.0.1:8000/
   ```bash
   docker run -p 8000:8000 mysite-minimal
   ```
3. Run with Docker compose to also test with Postgres connection
   ```bash
   docker compose up
   ```

## Fly deploy

To deploy this to [fly.io](https://fly.io):

1. Use `fly launch` to detect Django project and deploy database
   ```bash
   fly launch
   ```
   Ignore overwrites for `.dockerignore`, `Dockerfile` and tweak settings to set up a Postgres database (Fly Postgres, development)
