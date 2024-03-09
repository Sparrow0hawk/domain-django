import os

import dj_database_url
from dotenv import load_dotenv

from mysite.settings import *

load_dotenv()

DEBUG = False

ALLOWED_HOSTS: List[str] = ["django-polls.fly.dev"]

CSRF_TRUSTED_ORIGINS: List[str] = ["django-polls"]

SECRET_KEY = os.environ["SECRET_KEY"]

DATABASES["default"] = dj_database_url.config(
    default=os.environ["DATABASE_URL"], conn_max_age=600, conn_health_checks=True
)
