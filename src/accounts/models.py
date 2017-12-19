from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not full_name:
            raise ValueError("Users must have a full name")

        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name
        )
        user.set_password(password) # change user password
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name=None, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            full_name = full_name,
            password = password
        ) 
        user.staff = True
        user.save(using=self._db)    
        return user

    def create_superuser(self, email, full_name=None, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            full_name = full_name,
            password = password
        ) 
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(max_length=255, unique=True)
    full_name       = models.CharField(max_length=255, blank=True, null=True) 
    active          = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False) # staff user non super
    admin           = models.BooleanField(default=False) 
    timestamp       = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #username
    REQUIRED_FIELDS = [] # Add other required fields

    objects = UserManager()

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    # "Does the user have a specific permission?"
    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    # "Does the user have permissions to view the app 'app_label'?"
    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True

    # "Is the user a member of staf?"
    @property
    def is_staff(self):
        return self.staff

    # "Is the user an admin member?"
    @property
    def is_admin(self):
        return self.admin

    # "Is the user active?"
    @property
    def is_active(self):
        return self.active


class GuestEmail(models.Model):
    email           = models.EmailField()
    active          = models.BooleanField(default=True)
    update          = models.DateTimeField(auto_now=True)
    timestap        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

