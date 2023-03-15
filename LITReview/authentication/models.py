from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, PermissionsMixin
from django.db import models


class MyCustomManager(BaseUserManager):
    
    def create_user(self, username, email="", password=None, **extra_fields):
        """
        Creates and saves a User with a UserName, and a password.
        """
        
        if not username:
            raise ValueError('Users must have an username address')
        username = MyUser.normalize_username(username)
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, and password.
        """
        user = self.create_user(
            username=username,
            password=password,
            **extra_fields
        )
        user.groups.set('administrator')
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
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=SUBSCRIBER, verbose_name='Rôle')
    REQUIRED_FIELDS = []
    
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
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.role == self.ADMINISTRATOR:
    #         group = Group.objects.get(name='administrators')
    #         group.user_set.add(self)
    #     elif self.role == self.SUBSCRIBER:
    #         group = Group.objects.get(name='subscribers')
    #         group.user_set.add(self)
    #
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    class Meta:
        permissions = [
            ('see_all', 'Can see all tickets and reviews')
        ]
