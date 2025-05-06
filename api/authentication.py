from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        if not auth_header.startswith('Token '):
            raise AuthenticationFailed('Invalid token header. Must start with "Token "')

        token_key = auth_header[len('Token '):].strip()
        return self.authenticate_credentials(token_key)

    def authenticate_credentials(self, token_key):
        from markets.models import CustomToken  # avoid circular import
        try:
            token = CustomToken.objects.select_related('market').get(key=token_key)
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.market.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        return (token.market, token)

    def authenticate_header(self, request):
        return 'Token'
