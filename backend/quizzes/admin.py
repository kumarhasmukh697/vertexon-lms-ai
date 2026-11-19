from django.contrib import admin
from .models import ( Quiz, Question, Option, QuizAttempt, StudentAnswer,)




class OptionInline(admin.TabularInline):
    model = Option
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'course', 'duration_minutes', 'is_published',)
    list_filter = ('is_published',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'marks', 'order')
    inlines = [OptionInline]



@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'question', 'is_correct')




@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student','quiz', 'score', 'percentage', 'passed', 'status',)
    list_filter = ('status', 'passed')



@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt','question','selected_option','is_correct','awarded_marks',)
