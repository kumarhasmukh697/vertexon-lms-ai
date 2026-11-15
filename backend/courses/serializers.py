from rest_framework import serializers
from .models import Category, Course





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']




class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField( source='instructor.full_name', read_only=True)
    category_name = serializers.CharField( source='category.name', read_only=True)

    class Meta:
        model = Course
        fields = [ 'id', 'instructor', 'instructor_name', 'category', 'category_name', 'title',
            'description', 'thumbnail', 'difficulty', 'price', 'status', 'created_at', 'updated_at',
        ]

        read_only_fields = [ 'id', 'instructor', 'instructor_name', 'category_name', 'status', 'created_at', 'updated_at',]







# This ensures the admin can only set the status to approved or rejected through this API.
class CourseApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'status']
        read_only_fields = ['id', 'title']

    def validate_status(self, value):
        if value not in [
            Course.Status.APPROVED,
            Course.Status.REJECTED
        ]:
            raise serializers.ValidationError(
                "Status must be approved or rejected."
            )
        return value
