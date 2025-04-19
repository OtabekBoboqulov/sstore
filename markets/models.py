from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings


class CustomToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='custom_tokens', on_delete=models.CASCADE,
                             null=True)
    market = models.ForeignKey('Market', related_name='custom_tokens', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class MarketManager(BaseUserManager):
    def create_user(self, user_id, display_name, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID field must be set')
        user = self.model(user_id=user_id, display_name=display_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, display_name, password=None, **extra_fields):
        raise NotImplementedError("Use default User model for superusers")


class Market(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=16, unique=True)
    market_name = models.CharField(max_length=250)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    plan = models.CharField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='market_groups',  # Unique reverse accessor
        blank=True,
        help_text='The groups this market belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='market_permissions',  # Unique reverse accessor
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    objects = MarketManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['market_name']

    def __str__(self):
        return self.market_name
