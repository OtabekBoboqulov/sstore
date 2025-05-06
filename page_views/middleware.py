from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed
from api.authentication import CustomTokenAuthentication


@database_sync_to_async
def authenticate_token(token_key):
    auth = CustomTokenAuthentication()
    return auth.authenticate_credentials(token_key)


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        token = None

        if "token=" in query_string:
            token = query_string.split("token=")[-1]

        if token:
            try:
                user, _ = await authenticate_token(token)
            except AuthenticationFailed:
                user = AnonymousUser()
        else:
            user = AnonymousUser()

        scope["user"] = user
        return await super().__call__(scope, receive, send)
