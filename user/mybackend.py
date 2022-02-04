from django.contrib.auth.backends import ModelBackend
from .models import MyUser


class MobileBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        mobile = kwargs['mobile']
        try:
            user = MyUser.objects.get(mobile=mobile)
        except MyUser.DoesNotExist:
            pass
