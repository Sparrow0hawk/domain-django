from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Concatenate
from django.conf import settings
from django.http import HttpResponse, HttpRequest

T = TypeVar("T")
P = ParamSpec("P")


def api_key_auth(
    func: Callable[Concatenate[HttpRequest, P], T]
) -> Callable[Concatenate[HttpRequest, P], T | HttpResponse]:
    @wraps(func)
    def decorated_function(request: HttpRequest, /, *args: P.args, **kwargs: P.kwargs) -> T | HttpResponse:
        api_key = settings.API_KEY if settings.API_KEY else None
        auth = request.META.get("HTTP_AUTHORIZATION")
        if not _check_api_auth(auth, api_key):
            return HttpResponse(status=401)

        return func(request, *args, **kwargs)

    return decorated_function


def _check_api_auth(auth: str | None, api_key: str | None) -> bool:
    if not auth or len(auth.split()) < 2:
        return False

    auth_type, auth_token = auth.split()
    if not (auth_type.lower() == "api-key" and auth_token == api_key):
        return False

    return True
