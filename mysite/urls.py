"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

import polls.views
import polls.views.index
import polls.views.question_api
import polls.views.question_details
import polls.views.question_results

urlpatterns = [
    path("", polls.views.index.index, name="index"),
    path("<int:question_id>/", polls.views.question_details.question_details, name="question_details"),
    path("<int:question_id>/results", polls.views.question_results.question_results, name="question_results"),
    path("polls/questions", polls.views.question_api.questions_api, name="polls_questions"),
    path("admin/", admin.site.urls),
]
