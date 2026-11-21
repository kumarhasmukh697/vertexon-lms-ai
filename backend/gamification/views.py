from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    StudentPoints, PointTransaction, Badge,
    StudentBadge, LearningStreak,
)

from .serializers import (
    PointTransactionSerializer, BadgeSerializer,
    StudentBadgeSerializer, GamificationSummarySerializer,
    LeaderboardSerializer,
)




def ensure_student(user):
    if user.role != 'student':
        raise PermissionDenied( "This feature is available only to students.")



class GamificationSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        ensure_student(request.user)
        points, _ = StudentPoints.objects.get_or_create( student=request.user)
        streak, _ = LearningStreak.objects.get_or_create( student=request.user)
        earned_badges = StudentBadge.objects.filter( student=request.user).select_related('badge')

        data = {
            'total_points': points.total_points,
            'current_streak': streak.current_streak,
            'longest_streak': streak.longest_streak,
            'earned_badges': earned_badges,
        }

        serializer = GamificationSummarySerializer(data)
        return Response(serializer.data)




class PointHistoryView(generics.ListAPIView):

    serializer_class = PointTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        ensure_student(self.request.user)
        return PointTransaction.objects.filter( student=self.request.user)




class BadgeListView(generics.ListAPIView):

    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ensure_student(self.request.user)
        return Badge.objects.filter( is_active=True)





class MyBadgesView(generics.ListAPIView):

    serializer_class = StudentBadgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ensure_student(self.request.user)
        return StudentBadge.objects.filter( student=self.request.user).select_related('badge')





class LeaderboardView(generics.ListAPIView):

    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ensure_student(self.request.user)

        return StudentPoints.objects.filter( student__role='student'
        ).select_related('student').order_by(
            '-total_points'
        )[:10]
