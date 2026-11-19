from django.urls import path
from .views import ( AssignmentListCreateView, AssignmentDetailView, AssignmentSubmissionView, AssignmentSubmissionListView, GradeSubmissionView,MyAssignmentResultsView,)






urlpatterns = [

    # Instructor: list and create assignments
    path('courses/<uuid:course_id>/assignments/', AssignmentListCreateView.as_view(), name='assignment-list-create'),

    # Retrieve, update, and delete assignment
    path( 'assignments/<uuid:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),

    # Student: submit or update assignment
    path('assignments/<uuid:assignment_id>/submit/', AssignmentSubmissionView.as_view(), name='assignment-submit'),

    # Instructor: view submissions
    path('assignments/<uuid:assignment_id>/submissions/', AssignmentSubmissionListView.as_view(), name='assignment-submissions'),

    # Instructor: grade submission
    path('submissions/<uuid:submission_id>/grade/', GradeSubmissionView.as_view(), name='submission-grade'),

    # Student: view own results
    path('submissions/me/', MyAssignmentResultsView.as_view(), name='my-assignment-results'),

    
]
