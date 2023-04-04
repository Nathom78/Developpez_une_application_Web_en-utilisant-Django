from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyCustomManager(BaseUserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})
    
    def create_user(self, username, role, email, password=None, **extra_fields):
        """
        Creates and saves a User with a UserName, role(by default SUBSCRIBER), email(not obligatory) and a password.
        """
        
        if not username:
            raise ValueError(_('Users must have an username'))
        username = MyUser.normalize_username(username)
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email(not obligatory) and password.
        With role ADMINISTRATOR for superuser.
        """
        user = self.create_user(
            username=username,
            email=email,
            role='ADMINISTRATOR',
            password=password,
            **extra_fields
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    ADMINISTRATOR = 'ADMINISTRATOR'
    SUBSCRIBER = 'SUBSCRIBER'
    ROLE_CHOICES = [
        (ADMINISTRATOR, 'Administrateur'),
        (SUBSCRIBER, 'Utilisateur'),
    ]
    REQUIRED_FIELDS = ['email']
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=SUBSCRIBER, verbose_name='Rôle')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = MyCustomManager()
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def save(self, *args, **kwargs):
        
        if self.role == self.ADMINISTRATOR:
            self.is_admin = True
            super().save(*args, **kwargs)
            group = Group.objects.get(name='administrators')
            group.user_set.add(self)
        
        elif self.role == self.SUBSCRIBER:
            super().save(*args, **kwargs)
            group = Group.objects.get(name='subscribers')
            group.user_set.add(self)
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
