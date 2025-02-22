from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum


# define some account types
class AccountType(Enum):
    USER = "user"
    ADMIN = "admin"

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
    reward_pts = models.PositiveIntegerField(default=0)

    # Makes account type choices from the Enum and set default as USER
    account_type = models.CharField(
        max_length=10, choices=[(tag.value, tag.name) for tag in AccountType], default=AccountType.USER.value
    )


    def __str__(self):
        return self.username
