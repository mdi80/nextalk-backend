from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.cache import cache


class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone_token=None, **kwargs):
        UserModel = get_user_model()
        if phone_token is None:
            if "username" in kwargs:
                try:
                    phone = kwargs["username"]
                except:
                    return None
        else:
            phone = cache.get("auth " + phone_token)
            cache.delete("auth " + phone_token)

        if phone is not None:
            try:
                user = UserModel.objects.get(phone=phone)
                return user
            except UserModel.DoesNotExist:
                return None
        else:
            return None
    