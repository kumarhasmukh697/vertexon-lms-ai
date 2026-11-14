from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.



@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = ('email', 'full_name','role', 'is_verified','is_active',)
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('full_name','role','phone_number', 'profile_picture','is_verified',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'full_name', 'role',)
        }),
    )
