from channels.auth import AuthMiddlewareStack
from knox.models import AuthToken
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddlewareStack:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        print(scope["headers"])
        if b"authorization" in headers:
            try:
                token_name, token_key = headers[b"authorization"].decode().split()
                if token_name == "Token":
                    print("here")
                    token = AuthToken.objects.get(key=token_key)
                    scope["user"] = token.user
            except AuthToken.DoesNotExist:
                scope["user"] = AnonymousUser()
        return self.inner(scope, receive, send)


# TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
