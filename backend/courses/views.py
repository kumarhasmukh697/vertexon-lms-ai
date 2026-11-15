from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer
from accounts.permissions import ( IsAdmin, IsInstructorOrAdmin, IsCourseOwnerOrAdmin,)

# Create your views here.






class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]

        return [AllowAny()]


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInstructorOrAdmin()]

        return [AllowAny()]

    def get_queryset(self):
        return Course.objects.filter(
            status=Course.Status.APPROVED
        ).select_related('instructor', 'category')

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and (
            user.is_superuser or user.role == 'admin'
        ):
            return Course.objects.all()

        if user.is_authenticated and user.role == 'instructor':
            return Course.objects.filter(instructor=user)

        return Course.objects.filter(status=Course.Status.APPROVED)

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsCourseOwnerOrAdmin()]

        return [AllowAny()]
