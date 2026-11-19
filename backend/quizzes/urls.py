from django.urls import path
from .views import ( QuizListCreateView, QuizDetailView, QuestionListCreateView, StartQuizAttemptView, SubmitQuizAttemptView, MyQuizAttemptsView,)



urlpatterns = [

    # List and create quizzes for a course
    path( 'courses/<uuid:course_id>/quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),

    # Retrieve, update, or delete a quiz
    path('quizzes/<uuid:pk>/', QuizDetailView.as_view(), name='quiz-detail'),

    # List and create questions
    path( 'quizzes/<uuid:quiz_id>/questions/', QuestionListCreateView.as_view(), name='question-list-create'),

    # Start a quiz attempt
    path('quizzes/<uuid:quiz_id>/start/', StartQuizAttemptView.as_view(), name='quiz-start'),

    # Submit answers
    path('attempts/<uuid:attempt_id>/submit/', SubmitQuizAttemptView.as_view(), name='quiz-submit'),

    # View my quiz results
    path('attempts/me/', MyQuizAttemptsView.as_view(), name='my-quiz-attempts'),
    
]
