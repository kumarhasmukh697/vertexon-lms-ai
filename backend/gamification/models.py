import uuid

from django.db import models
from django.conf import settings





class StudentPoints(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='points')
    total_points = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.email} - {self.total_points} points"




class PointTransaction(models.Model):

    class ActivityType(models.TextChoices):
        LECTURE = 'lecture', 'Lecture Completed'
        QUIZ = 'quiz', 'Quiz Completed'
        ASSIGNMENT = 'assignment', 'Assignment Submitted'
        STREAK = 'streak', 'Learning Streak'
        BONUS = 'bonus', 'Bonus Points'

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='point_transactions')
    activity_type = models.CharField( max_length=20, choices=ActivityType.choices )
    points = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    # Identifies the activity that earned these points.
    # Examples: lecture UUID, quiz attempt UUID.
    source_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'activity_type', 'source_id'],
                name='unique_student_point_activity'
            )
        ]

        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.email} - {self.points} points"





class Badge(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    points_required = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name






class StudentBadge(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey( Badge, on_delete=models.CASCADE, related_name='recipients')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'badge'],
                name='unique_student_badge'
            )
        ]

    def __str__(self):
        return f"{self.student.email} - {self.badge.name}"





class LearningStreak(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_streak')
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.student.email} - "
            f"{self.current_streak} day streak"
        )
