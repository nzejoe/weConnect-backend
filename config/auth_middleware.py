from django.contrib.auth.models import AnonymousUser
from django.forms import ValidationError

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

from accounts.models import Account


@database_sync_to_async
def get_user(user_id):
    try:
        return Account.object.get(id=user_id)
    except (Account.DoesNotExist, ValidationError):
        return AnonymousUser()


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        user_id = parse_qs(scope['query_string'].decode('utf8'))['user_id'][0]
        scope['user'] = await get_user(user_id)

        return await self.app(scope, receive, send)