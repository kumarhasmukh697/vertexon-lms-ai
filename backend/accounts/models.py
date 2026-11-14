import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.






class User(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        INSTRUCTOR = 'instructor', 'Instructor'
        ADMIN = 'admin', 'Admin'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField( max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField( max_length=20,choices=Role.choices,default=Role.STUDENT)
    phone_number = models.CharField( max_length=20,blank=True)
    profile_picture = models.ImageField( upload_to='profile_pictures/', blank=True,null=True)
    is_verified = models.BooleanField( default=False)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email

