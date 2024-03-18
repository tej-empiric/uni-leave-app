from django.contrib.auth.backends import ModelBackend
from .models import MyUser


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):

        try:
            user = MyUser.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except MyUser.DoesNotExist:
            return None
