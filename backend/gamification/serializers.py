from rest_framework import serializers
from .models import (
    StudentPoints, PointTransaction, Badge,
    StudentBadge, LearningStreak,
)




class PointTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PointTransaction
        fields = [ 'id', 'activity_type', 'points', 'description', 'created_at',]
        read_only_fields = fields




class BadgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Badge
        fields = [ 'id', 'name', 'description', 'icon', 'points_required',]
        read_only_fields = fields




class StudentBadgeSerializer(serializers.ModelSerializer):

    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = StudentBadge
        fields = ['id', 'badge', 'earned_at',]
        read_only_fields = fields



class StudentPointsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentPoints
        fields = ['total_points', 'updated_at',]
        read_only_fields = fields




class LearningStreakSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearningStreak
        fields = ['current_streak', 'longest_streak', 'last_activity_date',]
        read_only_fields = fields



class GamificationSummarySerializer(serializers.Serializer):

    total_points = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    earned_badges = StudentBadgeSerializer(many=True)





class LeaderboardSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField( source='student.full_name', read_only=True)

    class Meta:
        model = StudentPoints
        fields = [ 'student_name', 'total_points',]
        read_only_fields = fields
