from rest_framework import serializers
from .models import Assignment, Submission





class AssignmentInstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = [ 'id', 'course', 'title', 'description', 'instructions', 'attachment',
            'max_marks','deadline','is_published','created_at','updated_at',
        ]

        read_only_fields = ['id','course','created_at','updated_at',]

    def validate_max_marks(self, value):
        if value <= 0:
            raise serializers.ValidationError("Maximum marks must be greater than zero.")
        return value





class AssignmentStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ['id','title','description','instructions','attachment','max_marks', 'deadline','created_at',]
        read_only_fields = fields





class SubmissionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = [ 'id', 'submission_text', 'submitted_file', 'submitted_at', 'status',]
        read_only_fields = [ 'id', 'submitted_at', 'status',]


    def validate(self, attrs):
        submission_text = attrs.get('submission_text', '')
        submitted_file = attrs.get('submitted_file')

        if not submission_text.strip() and not submitted_file:
            raise serializers.ValidationError("Provide submission text or upload a file.")
        return attrs




class SubmissionGradingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = [ 'id', 'marks_obtained', 'feedback', 'status', 'graded_at',]
        read_only_fields = ['id', 'status', 'graded_at',]

    def validate_marks_obtained(self, value):
        assignment = self.instance.assignment

        if value is None:
            raise serializers.ValidationError("Marks are required for grading.")

        if value < 0 or value > assignment.max_marks:
            raise serializers.ValidationError( f"Marks must be between 0 and {assignment.max_marks}.")

        return value









class SubmissionInstructorSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField( source='student.full_name', read_only=True)
    student_email = serializers.EmailField(source='student.email',  read_only=True)

    class Meta:
        model = Submission
        fields = ['id','student','student_name','student_email','submission_text','submitted_file',
            'status', 'marks_obtained', 'feedback', 'submitted_at', 'graded_at',
        ]





class StudentSubmissionResultSerializer(serializers.ModelSerializer):

    assignment_title = serializers.CharField( source='assignment.title', read_only=True)
    max_marks = serializers.IntegerField( source='assignment.max_marks', read_only=True)

    class Meta:
        model = Submission
        fields = [ 'id', 'assignment', 'assignment_title',
            'status','marks_obtained','max_marks','feedback',
            'submitted_at', 'graded_at',
        ]
        read_only_fields = fields
