import uuid
from django.db import models
from django.conf import settings




class Notification(models.Model):

    class NotificationType(models.TextChoices):
        GENERAL = 'general', 'General'
        COURSE = 'course', 'Course Update'
        LECTURE = 'lecture', 'New Lecture'
        ASSIGNMENT = 'assignment', 'Assignment'
        DEADLINE = 'deadline', 'Deadline Reminder'
        QUIZ = 'quiz', 'Quiz Result'
        GRADE = 'grade', 'Assignment Grade'

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField( max_length=20, choices=NotificationType.choices, default=NotificationType.GENERAL)

    # Optional URL or frontend route related to the notification.
    link = models.CharField( max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.email} - {self.title}"
