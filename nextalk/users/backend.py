from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        UserModel = get_user_model()
        if phone is None:
            if "username" in kwargs:
                try:
                    phone = kwargs["username"]
                except:
                    return None

        if phone is not None and password is not None:
            try:
                user = UserModel.objects.get(phone=phone)
                user.check_password(password)
                return user
            except UserModel.DoesNotExist:
                return None
        else:
            return None
