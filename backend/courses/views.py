from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, Course, Module, Lecture
from .serializers import CategorySerializer, CourseSerializer, CourseApprovalSerializer, ModuleSerializer, LectureSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied
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





class ModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer

    def get_course(self):
        return get_object_or_404( Course, id=self.kwargs['course_id'])


    def get_queryset(self):
        course = self.get_course()

        # Only show modules of approved courses
        # to users who are not the owner or an admin.
        user = self.request.user

        if user.is_authenticated and ( user.is_superuser or user.role == 'admin'):
            return Module.objects.filter(course=course)

        if user.is_authenticated and ( user.role == 'instructor' and course.instructor == user):
            return Module.objects.filter(course=course)

        return Module.objects.filter( course=course, course__status=Course.Status.APPROVED)


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInstructorOrAdmin()]

        return [AllowAny()]


    def perform_create(self, serializer):
        course = self.get_course()
        user = self.request.user

        if not ( user.is_superuser or user.role == 'admin' or course.instructor == user):
            raise PermissionDenied("You cannot add modules to this course.")

        if course.status != Course.Status.APPROVED and not ( user.is_superuser or user.role == 'admin'):
            raise PermissionDenied("The course must be approved before adding modules.")

        serializer.save(course=course)


class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ModuleSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and ( user.is_superuser or user.role == 'admin'):
            return Module.objects.all()

        if user.is_authenticated and user.role == 'instructor':
            return Module.objects.filter(course__instructor=user)

        return Module.objects.filter(course__status=Course.Status.APPROVED)


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsInstructorOrAdmin()]

        return [AllowAny()]


    def perform_update(self, serializer):
        module = self.get_object()
        user = self.request.user

        if not (user.is_superuser or user.role == 'admin' or module.course.instructor == user):
            raise PermissionDenied("You cannot update this module.")

        serializer.save()


    def perform_destroy(self, instance):
        user = self.request.user

        if not ( user.is_superuser or user.role == 'admin' or instance.course.instructor == user):
            raise PermissionDenied( "You cannot delete this module.")

        instance.delete()








class CourseApprovalView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseApprovalSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['patch', 'options', 'head']







class LectureListCreateView(generics.ListCreateAPIView):
    serializer_class = LectureSerializer

    def get_module(self):
        return get_object_or_404( Module, id=self.kwargs['module_id'])


    def get_queryset(self):
        module = self.get_module()
        user = self.request.user

        if user.is_authenticated and (user.is_superuser or user.role == 'admin'):
            return Lecture.objects.filter(module=module)

        if user.is_authenticated and ( user.role == 'instructor' and module.course.instructor == user):
            return Lecture.objects.filter(module=module)

        return Lecture.objects.filter( module=module, module__course__status=Course.Status.APPROVED)


    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsInstructorOrAdmin()]

        return [AllowAny()]



    def perform_create(self, serializer):
        module = self.get_module()
        user = self.request.user

        if not ( user.is_superuser or user.role == 'admin' or module.course.instructor == user):
            raise PermissionDenied("You cannot add lectures to this module.")

        if module.course.status != Course.Status.APPROVED and not ( user.is_superuser or user.role == 'admin'):
            raise PermissionDenied( "The course must be approved before adding lectures.")

        serializer.save(module=module)



class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and ( user.is_superuser or user.role == 'admin'):
            return Lecture.objects.all()

        if user.is_authenticated and user.role == 'instructor':
            return Lecture.objects.filter(module__course__instructor=user)

        return Lecture.objects.filter(module__course__status=Course.Status.APPROVED)


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsInstructorOrAdmin()]

        return [AllowAny()]


    def perform_update(self, serializer):
        lecture = self.get_object()
        user = self.request.user

        if not ( user.is_superuser or user.role == 'admin' or lecture.module.course.instructor == user):
            raise PermissionDenied( "You cannot update this lecture.")

        serializer.save()


    def perform_destroy(self, instance):
        user = self.request.user

        if not ( user.is_superuser or user.role == 'admin' or instance.module.course.instructor == user):
            raise PermissionDenied("You cannot delete this lecture.")

        instance.delete()
