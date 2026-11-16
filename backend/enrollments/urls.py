from django.urls import path
from .views import ( CourseEnrollmentView, MyEnrollmentsView, LectureProgressView,)



urlpatterns = [

    path( 'courses/<uuid:course_id>/enroll/', CourseEnrollmentView.as_view(), name='course-enroll'),
    path( 'enrollments/me/', MyEnrollmentsView.as_view(), name='my-enrollments'),
    path( 'lectures/<uuid:lecture_id>/progress/', LectureProgressView.as_view(), name='lecture-progress'),
    
]
