import os
from typing import List

import dj_database_url

from mysite.settings import *

DEBUG = False

ALLOWED_HOSTS.append("django-polls.fly.dev")

CSRF_TRUSTED_ORIGINS: List[str] = ["django-polls"]

SECRET_KEY = os.environ["SECRET_KEY"]

DATABASES["default"] = dj_database_url.config(
    default=os.environ["DATABASE_URL"], conn_max_age=600, conn_health_checks=True
)
