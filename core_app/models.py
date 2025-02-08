from django.contrib.auth.models import AbstractUser
from django.db import models


# The database table for user data
class UserAccount(AbstractUser):
    '''
    The AbstractUser class we extend provides fields:
    username, first_name, last_name, email, password, groups, user_permissions, is_staff,
    is_active, is_superuser, last_login, date_joined
    '''
    '''
    example of how to add additional attributes
    pts = models.PositiveIntegerField(default=0)
    '''
    def __str__(self):
        return self.username
