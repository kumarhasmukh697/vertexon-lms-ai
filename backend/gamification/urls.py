from django.urls import path
from .views import (
    GamificationSummaryView, PointHistoryView,
    BadgeListView, MyBadgesView, LeaderboardView,
)




urlpatterns = [

    # Student's complete gamification dashboard
    path('me/', GamificationSummaryView.as_view(), name='gamification-summary'),


    # Student's points history
    path('points/history/', PointHistoryView.as_view(), name='point-history'),

    # All available badges
    path( 'badges/', BadgeListView.as_view(), name='badge-list'),

    # Badges earned by the logged-in student
    path('badges/me/', MyBadgesView.as_view(), name='my-badges'),

    # Top 10 students
    path( 'leaderboard/', LeaderboardView.as_view(), name='leaderboard'),

]
