from django.contrib import admin
from .models import ( StudentPoints, PointTransaction, Badge, StudentBadge, LearningStreak,)


@admin.register(StudentPoints)
class StudentPointsAdmin(admin.ModelAdmin):
    list_display = ('student', 'total_points', 'updated_at')
    search_fields = ('student__email',)


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ('student','activity_type', 'points', 'source_id', 'created_at',)
    list_filter = ('activity_type', 'created_at')
    search_fields = ('student__email', 'description')


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name','points_required','is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(StudentBadge)
class StudentBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'earned_at')
    search_fields = ('student__email', 'badge__name')


@admin.register(LearningStreak)
class LearningStreakAdmin(admin.ModelAdmin):
    list_display = ('student','current_streak','longest_streak','last_activity_date',)
    search_fields = ('student__email',)
