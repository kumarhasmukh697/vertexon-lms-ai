from django.urls import path
from .views import ( CategoryListCreateView, CourseListCreateView, CourseDetailView, CourseApprovalView,  ModuleListCreateView, ModuleDetailView, LectureListCreateView, LectureDetailView, )






urlpatterns = [

    path('categories/',CategoryListCreateView.as_view(),name='category-list-create'),

    # Course URLs
    path('',CourseListCreateView.as_view(),name='course-list-create'),
    path('<uuid:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<uuid:pk>/approve/',CourseApprovalView.as_view(),name='course-approval'),
    
    # Module URLs
    path('<uuid:course_id>/modules/',ModuleListCreateView.as_view(),name='module-list-create'),
    path('modules/<uuid:pk>/',ModuleDetailView.as_view(),name='module-detail'),


    # Lecture URLs
    path('modules/<uuid:module_id>/lectures/', LectureListCreateView.as_view(), name='lecture-list-create'),
    path('lectures/<uuid:pk>/', LectureDetailView.as_view(), name='lecture-detail'),
    
]
