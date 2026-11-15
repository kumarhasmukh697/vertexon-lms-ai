from django.urls import path
from .views import ( CategoryListCreateView, CourseListCreateView, CourseDetailView,)






urlpatterns = [

    path('categories/',CategoryListCreateView.as_view(),name='category-list-create'),
    path('',CourseListCreateView.as_view(),name='course-list-create'),
    path('<uuid:pk>/', CourseDetailView.as_view(), name='course-detail'),
    
]
