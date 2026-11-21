from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone

from notifications.services import create_notification
from notifications.models import Notification

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from enrollments.models import Enrollment

from .models import ( Quiz, Question, Option, QuizAttempt, StudentAnswer,)

from .serializers import (QuizInstructorSerializer, QuizStudentSerializer, QuestionInstructorSerializer, QuestionStudentSerializer, QuizAttemptSerializer,)


from gamification.services import ( award_points, update_learning_streak,)
from gamification.models import PointTransaction



def is_admin(user):
    return user.is_authenticated and ( user.is_superuser or user.role == 'admin')


def is_course_instructor(user, course):
    return user.is_authenticated and ( user.role == 'instructor' and course.instructor_id == user.id)




class QuizListCreateView(generics.ListCreateAPIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]

        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.user.role == 'student':
            return QuizStudentSerializer

        return QuizInstructorSerializer

    def get_queryset(self):
        course = get_object_or_404( Course, id=self.kwargs['course_id'])

        user = self.request.user

        if is_admin(user):
            return Quiz.objects.filter(course=course)

        if is_course_instructor(user, course):
            return Quiz.objects.filter(course=course)

        if user.role == 'student':
            enrolled = Enrollment.objects.filter( student=user, course=course).exists()

            if enrolled and course.status == Course.Status.APPROVED:
                return Quiz.objects.filter( course=course, is_published=True).prefetch_related('questions__options')

        return Quiz.objects.none()


    def perform_create(self, serializer):
        course = get_object_or_404( Course, id=self.kwargs['course_id'])

        user = self.request.user

        if not ( is_admin(user) or is_course_instructor(user, course)):
            raise PermissionDenied( "You cannot create quizzes for this course.")


        if course.status != Course.Status.APPROVED:
            raise ValidationError( "Quizzes can only be created for approved courses.")

        serializer.save(course=course)




class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Quiz.objects.all()

        if user.role == 'instructor':
            return Quiz.objects.filter(course__instructor=user)

        if user.role == 'student':
            return Quiz.objects.filter(
                course__enrollments__student=user,
                course__enrollments__status=Enrollment.Status.ACTIVE,
                course__status=Course.Status.APPROVED,
                is_published=True
            ).distinct()

        return Quiz.objects.none()


    def get_serializer_class(self):
        if self.request.user.role == 'student':
            return QuizStudentSerializer

        return QuizInstructorSerializer


    def get_permissions(self):
        return [IsAuthenticated()]


    def perform_update(self, serializer):
        quiz = self.get_object()
        user = self.request.user

        if not ( is_admin(user) or is_course_instructor(user, quiz.course)):
            raise PermissionDenied( "You cannot update this quiz.")

        if quiz.is_published and not is_admin(user):
            raise PermissionDenied("Unpublish the quiz before editing it.")

        serializer.save()



    def perform_destroy(self, instance):
        user = self.request.user

        if not ( is_admin(user) or is_course_instructor(user, instance.course)):
            raise PermissionDenied( "You cannot delete this quiz.")

        instance.delete()




class QuestionListCreateView(generics.ListCreateAPIView):

    def get_quiz(self):
        return get_object_or_404( Quiz, id=self.kwargs['quiz_id'])

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.user.role == 'student':
            return QuestionStudentSerializer

        return QuestionInstructorSerializer

    def get_queryset(self):
        quiz = self.get_quiz()
        user = self.request.user

        if is_admin(user):
            return Question.objects.filter(quiz=quiz).prefetch_related('options')

        if is_course_instructor(user, quiz.course):
            return Question.objects.filter(quiz=quiz).prefetch_related( 'options')

        if user.role == 'student':
            enrolled = Enrollment.objects.filter(
                student=user, course=quiz.course, status=Enrollment.Status.ACTIVE ).exists()

            if enrolled and quiz.is_published:
                return Question.objects.filter( quiz=quiz).prefetch_related('options')

        return Question.objects.none()



    def perform_create(self, serializer):
        quiz = self.get_quiz()
        user = self.request.user

        if not ( is_admin(user) or is_course_instructor(user, quiz.course)):
            raise PermissionDenied("You cannot add questions to this quiz.")

        if quiz.is_published:
            raise ValidationError( "Unpublish the quiz before adding questions.")

        serializer.save(quiz=quiz)




class StartQuizAttemptView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):

        if request.user.role != 'student':
            raise PermissionDenied( "Only students can attempt quizzes.")

        quiz = get_object_or_404( Quiz, id=quiz_id, is_published=True, course__status=Course.Status.APPROVED)

        enrollment = get_object_or_404(
            Enrollment,student=request.user,course=quiz.course, status=Enrollment.Status.ACTIVE
        )

        if not quiz.questions.exists():
            raise ValidationError( "This quiz does not have any questions yet." )

        attempt = QuizAttempt.objects.create( student=request.user, quiz=quiz)

        return Response( QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)




class SubmitQuizAttemptView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, attempt_id):

        if request.user.role != 'student':
            raise PermissionDenied( "Only students can submit quiz attempts.")

        attempt = get_object_or_404(
            QuizAttempt.objects.select_for_update(),
            id=attempt_id, student=request.user, status=QuizAttempt.Status.IN_PROGRESS
        )

        answers = request.data.get('answers')

        if not isinstance(answers, list):
            raise ValidationError("Answers must be provided as a list.")

        if not answers:
            raise ValidationError( "Submit at least one answer.")

        question_ids = set()
        prepared_answers = []

        questions = {
            str(question.id): question
            for question in attempt.quiz.questions.all()
        }

        for answer in answers:

            question_id = str(answer.get('question', ''))
            option_id = answer.get('selected_option')

            if question_id in question_ids:
                raise ValidationError( "A question cannot be answered more than once.")

            question_ids.add(question_id)

            question = questions.get(question_id)

            if question is None:
                raise ValidationError( "One or more questions do not belong to this quiz." )

            option = get_object_or_404( Option, id=option_id, question=question)

            prepared_answers.append((question, option))

        total_marks = sum(question.marks for question in questions.values())

        score = 0

        for question, option in prepared_answers:

            correct = option.is_correct
            awarded = question.marks if correct else 0

            StudentAnswer.objects.create(
                attempt=attempt,question=question,
                selected_option=option, is_correct=correct,
                awarded_marks=awarded
            )

            score += awarded

        percentage = (
            (Decimal(score) / Decimal(total_marks)) * Decimal('100')
            if total_marks > 0 else Decimal('0')
        )

        attempt.score = score
        attempt.total_marks = total_marks
        attempt.percentage = percentage.quantize( Decimal('0.01'))
        attempt.passed = ( percentage >= attempt.quiz.passing_percentage)
        attempt.status = QuizAttempt.Status.SUBMITTED
        attempt.submitted_at = timezone.now()

        attempt.save()


        award_points(
            student=attempt.student,
            activity_type=PointTransaction.ActivityType.QUIZ,
            points=20,
            description=f"Completed quiz: {attempt.quiz.title}",
            source_id=attempt.id
        )

        update_learning_streak(attempt.student)


        create_notification(
            recipient=attempt.student,
            title="Quiz Result Available",
            message=(
                f"You completed '{attempt.quiz.title}'. "
                f"Your score is {attempt.score}/"
                f"{attempt.total_marks} "
                f"({attempt.percentage}%)."
            ),
            notification_type=Notification.NotificationType.QUIZ,
            link="/student/quizzes/"
        )

        return Response( QuizAttemptSerializer(attempt).data, status=status.HTTP_200_OK)



class MyQuizAttemptsView(generics.ListAPIView):

    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'student':
            raise PermissionDenied( "Only students can view their quiz attempts.")

        return QuizAttempt.objects.filter(
            student=self.request.user,
            status=QuizAttempt.Status.SUBMITTED
        ).select_related('quiz')
