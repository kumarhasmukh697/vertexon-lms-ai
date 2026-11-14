import uuid
from django.db import models
from django.conf import settings

# Create your models here.





# category model
class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



# course model
class Course(models.Model):

    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Approval'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    instructor = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey( Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField( upload_to='course_thumbnails/', blank=True, null=True)
    difficulty = models.CharField( max_length=20, choices=Difficulty.choices, default=Difficulty.BEGINNER)
    price = models.DecimalField( max_digits=10, decimal_places=2, default=0)
    status = models.CharField( max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




class Module(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey( Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title




class Lecture(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey( Module, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video = models.FileField( upload_to='lectures/videos/', blank=True, null=True)
    pdf_material = models.FileField( upload_to='lectures/pdfs/', blank=True, null=True)
    transcript = models.TextField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=1)
    is_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

