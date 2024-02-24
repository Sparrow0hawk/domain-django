from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest):
    return HttpResponse("<h1>Hello world!</h1>")
