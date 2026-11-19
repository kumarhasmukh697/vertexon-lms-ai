from rest_framework import serializers
from .models import ( Quiz, Question, Option, QuizAttempt, StudentAnswer,)




class OptionStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text']



class OptionInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']
        read_only_fields = ['id']




class QuestionStudentSerializer(serializers.ModelSerializer):
    options = OptionStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id','question_text','marks','order','options',]




class QuestionInstructorSerializer(serializers.ModelSerializer):
    options = OptionInstructorSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id','question_text','marks','order','options',]
        read_only_fields = ['id']

    def validate_options(self, value):
        if len(value) < 2:
            raise serializers.ValidationError( "A question must have at least two options.")

        correct_count = sum(1 for option in value if option.get('is_correct'))

        if correct_count != 1:
            raise serializers.ValidationError("Exactly one option must be marked correct.")

        return value

    def create(self, validated_data):
        options_data = validated_data.pop('options')

        question = Question.objects.create(**validated_data)

        for option_data in options_data:
            Option.objects.create(question=question, **option_data)

        return question





class QuizStudentSerializer(serializers.ModelSerializer):
    questions = QuestionStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [ 'id', 'title', 'description', 'duration_minutes', 'passing_percentage', 'questions',]





class QuizInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [ 'id', 'course', 'title', 'description', 'duration_minutes', 'passing_percentage','is_published','created_at',]
        read_only_fields = ['id', 'course', 'created_at']

    def validate_passing_percentage(self, value):
        if not 1 <= value <= 100:
            raise serializers.ValidationError("Passing percentage must be between 1 and 100.")
        return value




class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = [ 'id', 'quiz', 'status', 'score', 'total_marks', 'percentage', 'passed', 'started_at', 'submitted_at',]
        read_only_fields = fields



class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = [ 'question', 'selected_option',]
