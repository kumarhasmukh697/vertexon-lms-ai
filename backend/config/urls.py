from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzk0NjQ3MzgwLCJpYXQiOjE3OTQ2NDU1ODAsImp0aSI6IjYyOWRlYWEyZDlkNzQ1ODFhZGIxYTU4MDYxYjRmNTdhIiwidXNlcl9pZCI6IjRmOWViZTZmLTY5MjctNGMxNy1iZDZmLThhZGNjNmVmM2RmYiJ9.3JNIOFKpKEDZf3WZVKOj_DhB_3qFkgYw4HtsfpDJelg
