from rest_framework import serializers
from django.db.models import Count
from .models import Enrollment, LectureProgress






class EnrollmentSerializer(serializers.ModelSerializer):

    course_title = serializers.CharField(source='course.title', read_only=True)
    total_lectures = serializers.SerializerMethodField()
    completed_lectures = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [ 'id', 'course', 'course_title', 'status','enrolled_at',
            'completed_at','total_lectures',  'completed_lectures', 'progress_percentage',
        ]

        read_only_fields = fields


    def get_total_lectures(self, obj):
        return obj.course.modules.aggregate( total=Count('lectures'))['total'] or 0

    def get_completed_lectures(self, obj):
        return obj.lecture_progress.filter( is_completed=True).count()

    def get_progress_percentage(self, obj):
        total = self.get_total_lectures(obj)

        if total == 0:
            return 0

        completed = self.get_completed_lectures(obj)
        return round((completed / total) * 100, 2)






class LectureProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = LectureProgress
        fields = [ 'id', 'lecture', 'watched_seconds', 'is_completed', 'completed_at',
            'updated_at',
        ]

        read_only_fields = [ 'id', 'lecture', 'completed_at',
            'updated_at',
        ]


    def validate_watched_seconds(self, value):
        if value < 0:
            raise serializers.ValidationError( "Watched seconds cannot be negative.")
        return value
