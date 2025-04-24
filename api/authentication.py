from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from markets.models import CustomToken
import re


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None  # No header, skip authentication (returns AnonymousUser)

        # Expect header format: "Token <key>"
        if not auth_header.startswith('Token '):
            raise AuthenticationFailed('Invalid token header. Must start with "Token "')

        # Extract token key
        token_key = auth_header[len('Token '):].strip()
        if not token_key:
            raise AuthenticationFailed('Invalid token header. No token provided')

        # Look up the token
        try:
            token = CustomToken.objects.select_related('market').get(key=token_key)
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.market.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # Return (user, token) tuple as expected by DRF
        return (token.market, token)

    def authenticate_header(self, request):
        return 'Token'  # Informs client to use "Token" in Authorization header
