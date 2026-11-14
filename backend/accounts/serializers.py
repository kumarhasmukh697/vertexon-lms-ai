from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()


# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField( write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField( write_only=True)

    class Meta:
        model = User

        fields = ['id','username','full_name','email','password','confirm_password',]
        read_only_fields = ['id']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value.lower()

    def validate(self, attrs):

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):

        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            **validated_data,
            role=User.Role.STUDENT
        )

        return user








class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [ 'id', 'username', 'full_name', 'email', 'role', 'phone_number', 'profile_picture', 'is_verified', 'created_at',]
        read_only_fields = fields

