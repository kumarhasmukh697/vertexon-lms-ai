from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from enrollments.models import Enrollment

from .models import Assignment, Submission

from .serializers import ( AssignmentInstructorSerializer, AssignmentStudentSerializer, SubmissionCreateSerializer, SubmissionGradingSerializer, SubmissionInstructorSerializer, StudentSubmissionResultSerializer,)





def is_admin(user):
    return user.is_authenticated and ( user.is_superuser or user.role == 'admin')


def is_course_instructor(user, course):
    return user.is_authenticated and ( user.role == 'instructor' and course.instructor_id == user.id)






class AssignmentListCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    def get_course(self):
        return get_object_or_404( Course, id=self.kwargs['course_id'])

    def get_serializer_class(self):
        if self.request.user.role == 'student':
            return AssignmentStudentSerializer
        return AssignmentInstructorSerializer

    def get_queryset(self):
        course = self.get_course()
        user = self.request.user

        if is_admin(user):
            return Assignment.objects.filter(course=course)

        if is_course_instructor(user, course):
            return Assignment.objects.filter(course=course)

        if user.role == 'student':
            enrolled = Enrollment.objects.filter(student=user, course=course,status=Enrollment.Status.ACTIVE).exists()

            if enrolled and course.status == Course.Status.APPROVED:
                return Assignment.objects.filter(course=course, is_published=True)
        return Assignment.objects.none()



    def perform_create(self, serializer):
        course = self.get_course()
        user = self.request.user

        if not ( is_admin(user) or is_course_instructor(user, course)):
            raise PermissionDenied("You cannot create assignments for this course.")

        if course.status != Course.Status.APPROVED:
            raise ValidationError( "Assignments can only be created for approved courses.")

        serializer.save(course=course)







class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Assignment.objects.all()

        if user.role == 'instructor':
            return Assignment.objects.filter( course__instructor=user)

        if user.role == 'student':
            return Assignment.objects.filter(
                course__enrollments__student=user,
                course__enrollments__status=Enrollment.Status.ACTIVE,
                course__status=Course.Status.APPROVED,
                is_published=True
            ).distinct()

        return Assignment.objects.none()



    def get_serializer_class(self):
        if self.request.user.role == 'student':
            return AssignmentStudentSerializer

        return AssignmentInstructorSerializer


    def perform_update(self, serializer):
        assignment = self.get_object()
        user = self.request.user

        if not ( is_admin(user) or is_course_instructor(user, assignment.course)):
            raise PermissionDenied("You cannot update this assignment.")
        serializer.save()



    def perform_destroy(self, instance):
        user = self.request.user

        if not ( is_admin(user) or is_course_instructor(user, instance.course)):
            raise PermissionDenied("You cannot delete this assignment.")
        instance.delete()








class AssignmentSubmissionView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, assignment_id):

        if request.user.role != 'student':
            raise PermissionDenied( "Only students can submit assignments.")

        assignment = get_object_or_404( Assignment,
            id=assignment_id, is_published=True, course__status=Course.Status.APPROVED
        )

        enrollment = Enrollment.objects.filter(
            student=request.user, course=assignment.course, status=Enrollment.Status.ACTIVE
        ).first()

        if enrollment is None:
            raise PermissionDenied( "You must be enrolled in this course to submit.")

        if timezone.now() > assignment.deadline:
            raise ValidationError( "The submission deadline has passed.")

        existing_submission = Submission.objects.filter(
            assignment=assignment, student=request.user
        ).first()

        serializer = SubmissionCreateSerializer(
            instance=existing_submission, data=request.data,
            partial=existing_submission is not None
        )

        serializer.is_valid(raise_exception=True)

        submission = serializer.save(
            assignment=assignment, student=request.user,
            status=Submission.Status.SUBMITTED
        )

        # Reset previous grading if the student resubmits.
        submission.marks_obtained = None
        submission.feedback = ''
        submission.graded_at = None
        submission.submitted_at = timezone.now()

        submission.save()

        return Response(
            SubmissionCreateSerializer(submission).data,
            status=( status.HTTP_200_OK
                if existing_submission
                else status.HTTP_201_CREATED
            )
        )








class AssignmentSubmissionListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionInstructorSerializer

    def get_queryset(self):
        assignment = get_object_or_404( Assignment, id=self.kwargs['assignment_id'])

        user = self.request.user

        if not ( is_admin(user)  or is_course_instructor(user, assignment.course)):
            raise PermissionDenied( "You cannot view submissions for this assignment.")

        return Submission.objects.filter( assignment=assignment).select_related('student', 'assignment')







class GradeSubmissionView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request, submission_id):

        submission = get_object_or_404(
            Submission.objects.select_related('assignment__course'),
            id=submission_id
        )

        user = request.user

        if not ( is_admin(user) or is_course_instructor( user, submission.assignment.course)):
            raise PermissionDenied("You cannot grade this submission.")

        serializer = SubmissionGradingSerializer( submission,data=request.data,partial=True)

        serializer.is_valid(raise_exception=True)

        if 'marks_obtained' not in serializer.validated_data:
            raise ValidationError("Marks are required to grade a submission.")

        submission = serializer.save( status=Submission.Status.GRADED, graded_at=timezone.now())

        return Response( SubmissionInstructorSerializer(submission).data, status=status.HTTP_200_OK )







class MyAssignmentResultsView(generics.ListAPIView):

    serializer_class = StudentSubmissionResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'student':
            raise PermissionDenied( "Only students can view their assignment results.")

        return Submission.objects.filter(student=self.request.user).select_related('assignment')
