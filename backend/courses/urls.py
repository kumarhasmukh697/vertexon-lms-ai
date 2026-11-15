from django.urls import path
from .views import ( CategoryListCreateView, CourseListCreateView, CourseDetailView, CourseApprovalView, )






urlpatterns = [

    path('categories/',CategoryListCreateView.as_view(),name='category-list-create'),
    path('',CourseListCreateView.as_view(),name='course-list-create'),
    path('<uuid:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<uuid:pk>/approve/',CourseApprovalView.as_view(),name='course-approval'),
    
]
