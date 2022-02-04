from django.contrib.auth.base_user import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **other_fields):
        if not mobile:
            raise ValueError("mobile is required...!")
        user = self.model(mobile=mobile, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser muse have is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser muse have is_superuser=True')
        return self.create_user(mobile, password, **other_fields)
