# markets/backends.py
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from .models import Market


class CombinedAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try authenticating with Market first
        try:
            user = Market.objects.get(market_username=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Market.DoesNotExist:
            pass

        # Fallback to default User model
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        # Only check is_active, allow staff check for User model in admin
        return getattr(user, 'is_active', False)

    def get_user(self, user_id):
        # Try Market
        try:
            user = Market.objects.get(pk=user_id)
            if self.user_can_authenticate(user):
                return user
        except Market.DoesNotExist:
            pass

        # Fallback to default User
        try:
            user = User.objects.get(pk=user_id)
            if self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
