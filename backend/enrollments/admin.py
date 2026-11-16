from django.contrib import admin
from .models import Enrollment, LectureProgress





@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ( 'student', 'course', 'status', 'enrolled_at', 'completed_at',)
    list_filter = ('status', 'enrolled_at')
    search_fields = ( 'student__email', 'course__title',)




@admin.register(LectureProgress)
class LectureProgressAdmin(admin.ModelAdmin):
    list_display = ( 'enrollment', 'lecture', 'watched_seconds', 'is_completed','updated_at',)
    list_filter = ('is_completed',)

