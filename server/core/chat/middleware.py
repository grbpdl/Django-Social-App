

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(token_key):
    from django.contrib.auth.models import AnonymousUser
    from django.contrib.auth import get_user_model
    from rest_framework_simplejwt.tokens import AccessToken
    User = get_user_model()
    try:
        access_token = AccessToken(token_key)
        user = User.objects.get(id=access_token['user_id'])
        return user
    except Exception:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            # Get token from query string
            query_string = scope.get('query_string', b'').decode()
            query_params = dict(param.split('=') for param in query_string.split('&') if param)
            token = query_params.get('token', '')
            user = await get_user(token)
            # Only allow premium users
            if not getattr(user, 'is_premium', False):
                from django.contrib.auth.models import AnonymousUser
                scope['user'] = AnonymousUser()
            else:
                scope['user'] = user
        except:
            from django.contrib.auth.models import AnonymousUser
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
