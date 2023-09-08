from channels.auth import AuthMiddlewareStack
from knox.models import AuthToken
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async

from users.models import Ticket


@database_sync_to_async
def get_user(ticket):
    return Ticket.objects.get(ticket=ticket).token.user


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        ticket = scope["query_string"]

        scope["user"] = await get_user(scope["query_string"].decode())
        print(scope["user"])
        return self.inner(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
