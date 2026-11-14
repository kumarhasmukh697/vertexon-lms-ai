from django.contrib import admin
from .models import Category, Course, Module, Lecture

# Register your models here.




admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lecture)