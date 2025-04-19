from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from .models import Market


class CombinedAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try authenticating with default User model first for admin
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            pass

        # Fallback to Market using phone_number
        try:
            user = Market.objects.get(phone_number=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Market.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        # Check is_active for all users
        return getattr(user, 'is_active', False)

    def get_user(self, user_id):
        # Try default User
        try:
            user = User.objects.get(pk=user_id)
            if self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            pass

        # Fallback to Market
        try:
            user = Market.objects.get(pk=user_id)
            if self.user_can_authenticate(user):
                return user
        except Market.DoesNotExist:
            return None
