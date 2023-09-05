from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    # AbstractBaseUser
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.core.cache import cache
from knox.models import AuthToken
import unicodedata
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_key, **extra_fields):
        if not phone_key:
            raise ValueError("The phone field must be set")
        # cache.get("auth " + phone_key)
        phone = PhoneTokenTempModel.objects.get(phone_key=str(phone_key)).phone
        if phone is None:
            raise ValueError("phone token is expired!")

        user = self.model(phone=phone, **extra_fields)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if not phone:
            raise ValueError("The phone field must be set")

        if phone is None:
            raise ValueError("phone token is expired!")

        user = self.model(phone=phone, **extra_fields)
        user.save(using=self._db)

        return user


class CustomUserAbstract(models.Model):
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    is_active = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )


class User(CustomUserAbstract, PermissionsMixin):
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
    userid_validator = UnicodeUsernameValidator()

    userid = models.CharField(
        _("userid"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[userid_validator],
        error_messages={
            "unique": _("A user with that userid already exists."),
        },
        null=True,
    )
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Add other fields as needed

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.phone}"


class PhoneTokenTempModel(models.Model):
    phone_key = models.CharField(max_length=40, primary_key=True)
    phone = models.CharField(max_length=17)
