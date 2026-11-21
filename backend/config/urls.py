from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/courses/', include('courses.urls')),
    path('api/v1/', include('enrollments.urls')),
    path('api/v1/', include('quizzes.urls')),
    path('api/v1/', include('assignments.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/gamification/', include('gamification.urls')),
] 
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

