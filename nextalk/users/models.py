from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.core.cache import cache
from knox.models import AuthToken


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_key, password, **extra_fields):
        if not phone_key:
            raise ValueError("The phone field must be set")
        if not password:
            raise ValueError("The Password field must be set")

        phone = cache.get("auth " + phone_key)
        cache.delete("auth " + phone_key)
        if phone is None:
            raise ValueError("phone token is expired!")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=17,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r"^\+[\d]+$",  # Regex pattern to start with a plus sign and followed by digits
                message="Phone number must start with a plus sign (+) and consist of digits only.",
                code="invalid_phone_number",
            )
        ],
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Add other fields as needed

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.phone} {self.last_name}"


# class UserToken(models.Model):
#     key = models.CharField(_("Key"), max_length=40, primary_key=True)
#     user = models.OneToOneField(
#         User, related_name='auth_token',
#         on_delete=models.CASCADE, verbose_name=_("User")
#     )
#     created = models.DateTimeField(_("Created"), auto_now_add=True)

#     class Meta:
#         # Work around for a bug in Django:
#         # https://code.djangoproject.com/ticket/19422
#         #
#         # Also see corresponding ticket:
#         # https://github.com/encode/django-rest-framework/issues/705
#         abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
#         verbose_name = _("Token")
#         verbose_name_plural = _("Tokens")

#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super().save(*args, **kwargs)

#     @classmethod
#     def generate_key(cls):
#         return binascii.hexlify(os.urandom(20)).decode()

#     def __str__(self):
#         return self.key
