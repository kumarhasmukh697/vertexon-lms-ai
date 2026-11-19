import uuid
from django.db import models
from django.conf import settings





class Quiz(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey( 'courses.Course', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    passing_percentage = models.PositiveIntegerField(default=40)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





class Question(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey( Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    marks = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text[:80]

    class Meta:
        ordering = ['order']





class Option(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text





class QuizAttempt(models.Model):

    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        SUBMITTED = 'submitted', 'Submitted'

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey( Quiz, on_delete=models.CASCADE, related_name='attempts')
    status = models.CharField( max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    score = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)
    percentage = models.DecimalField( max_digits=5, decimal_places=2, default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.quiz.title}"






class StudentAnswer(models.Model):

    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey( QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey( Question, on_delete=models.CASCADE, related_name='student_answers')
    selected_option = models.ForeignKey( Option, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_answers')
    is_correct = models.BooleanField(default=False)
    awarded_marks = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['attempt', 'question'],
                name='unique_attempt_question_answer'
            )
        ]

    def __str__(self):
        return f"{self.attempt.student} - {self.question}"
