from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Lecture

from .models import Enrollment, LectureProgress
from .serializers import ( EnrollmentSerializer, LectureProgressSerializer,)





class CourseEnrollmentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):

        if request.user.role != 'student':
            raise PermissionDenied( "Only students can enroll in courses.")

        course = get_object_or_404( Course, id=course_id, status=Course.Status.APPROVED)

        # Payment integration is not implemented yet.
        if course.price > 0:
            raise ValidationError( "Payment is required before enrolling in this course.")


        if Enrollment.objects.filter( student=request.user, course=course).exists():
            raise ValidationError( "You are already enrolled in this course.")

        enrollment = Enrollment.objects.create( student=request.user, course=course)
        serializer = EnrollmentSerializer(enrollment)

        return Response( serializer.data, status=status.HTTP_201_CREATED)





class MyEnrollmentsView(generics.ListAPIView):

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'student':
            raise PermissionDenied( "Only students can view their enrollments.")

        return Enrollment.objects.filter(student=self.request.user).select_related('course').prefetch_related( 'lecture_progress')






class LectureProgressView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, lecture_id):

        if request.user.role != 'student':
            raise PermissionDenied("Only students can update learning progress.")

        lecture = get_object_or_404(
            Lecture.objects.select_related( 'module__course'),
            id=lecture_id,
            module__course__status=Course.Status.APPROVED
        )

        enrollment = get_object_or_404( Enrollment, student=request.user, course=lecture.module.course)

        if enrollment.status == Enrollment.Status.COMPLETED:
            raise ValidationError("This course has already been completed.")

        serializer = LectureProgressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        progress, created = LectureProgress.objects.get_or_create( enrollment=enrollment, lecture=lecture,
        defaults={
            **serializer.validated_data,
            'completed_at': ( timezone.now() if serializer.validated_data.get('is_completed', False) else None)
        }
        )

        if not created:
            new_watched_seconds = serializer.validated_data.get('watched_seconds', progress.watched_seconds)
            new_is_completed = serializer.validated_data.get('is_completed', progress.is_completed)
            progress.watched_seconds = max( progress.watched_seconds, new_watched_seconds)

            progress.is_completed = new_is_completed

            progress.completed_at = ( timezone.now() if new_is_completed else None)

            progress.save()

        # Update the overall enrollment status.
        total_lectures = Lecture.objects.filter( module__course=lecture.module.course).count()

        completed_lectures = LectureProgress.objects.filter( enrollment=enrollment, is_completed=True).count()

        if ( total_lectures > 0 and completed_lectures == total_lectures):
            enrollment.status = Enrollment.Status.COMPLETED
            enrollment.completed_at = timezone.now()
            enrollment.save( update_fields=['status', 'completed_at'])

        response_serializer = LectureProgressSerializer(progress)

        return Response( response_serializer.data, status=status.HTTP_200_OK)
