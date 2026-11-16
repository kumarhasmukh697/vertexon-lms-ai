import uuid
from django.db import models
from django.conf import settings




# Create your models here.






class Enrollment(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey( 'courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField( max_length=20, choices=Status.choices, default=Status.ACTIVE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField( null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course_enrollment'
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.course}"





class LectureProgress(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey( Enrollment, on_delete=models.CASCADE, related_name='lecture_progress')
    lecture = models.ForeignKey( 'courses.Lecture', on_delete=models.CASCADE, related_name='student_progress')
    watched_seconds = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField( null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['enrollment', 'lecture'],
                name='unique_enrollment_lecture_progress'
            )
        ]

    def __str__(self):
        return f"{self.enrollment.student} - {self.lecture.title}"

