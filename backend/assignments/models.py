import uuid
from django.db import models
from django.conf import settings





class Assignment(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField(blank=True)
    attachment = models.FileField( upload_to='assignments/materials/', blank=True, null=True)
    max_marks = models.PositiveIntegerField(default=100)
    deadline = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





class Submission(models.Model):

    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        GRADED = 'graded', 'Graded'

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey( Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignment_submissions')
    submission_text = models.TextField(blank=True)
    submitted_file = models.FileField( upload_to='assignments/submissions/', blank=True, null=True)
    status = models.CharField( max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    marks_obtained = models.PositiveIntegerField( null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)



    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['assignment', 'student'],
                name='unique_assignment_student_submission'
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
