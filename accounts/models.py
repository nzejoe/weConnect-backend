import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class AccountManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if not username:
            raise ValidationError('username field is required')

        if not email:
            raise ValidationError('email field is required')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # assign admin privileges
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):
    GENDER = (
        ('female', 'Female'),
        ('male', 'Male'),
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    avatar = ProcessedImageField(
        upload_to='users/', processors=[ResizeToFill(500, 500), ], format='JPEG', options={'quality': 60}, null=True, blank=True)
    # create thumbnail from avatar
    thumb = ImageSpecField(source='avatar', processors=[ResizeToFill(
        100, 100), ],  format='JPEG', options={'quality': 60})
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    
    object = AccountManager()
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def __str__(self):
        return self.username
