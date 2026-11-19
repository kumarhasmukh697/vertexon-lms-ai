from django.contrib import admin
from .models import Assignment, Submission





@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = ( 'title', 'course', 'max_marks', 'deadline', 'is_published',)
    list_filter = ('is_published', 'deadline')
    search_fields = ('title', 'course__title')



@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = ( 'student', 'assignment', 'status', 'marks_obtained', 'submitted_at',)
    list_filter = ('status', 'submitted_at')
    search_fields = ( 'student__email', 'assignment__title',)
