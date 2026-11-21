from django.db import transaction
from django.utils import timezone
from .models import (
    StudentPoints, PointTransaction, Badge,
    StudentBadge, LearningStreak,
)




@transaction.atomic
def award_points( student, activity_type, points, description, source_id):
    if points <= 0:
        raise ValueError("Points must be greater than zero.")

    # Create the student's points record if it doesn't exist.
    student_points, _ = StudentPoints.objects.get_or_create( student=student)

    # Lock the points record during the update.
    student_points = StudentPoints.objects.select_for_update().get(
        id=student_points.id
    )

    # Check whether this activity has already awarded points.
    transaction_record, created = PointTransaction.objects.get_or_create(
        student=student,
        activity_type=activity_type,
        source_id=str(source_id),
        defaults={
            'points': points,
            'description': description,
        }
    )

    if not created:
        return transaction_record

    # Update total points.
    student_points.total_points += points
    student_points.save(update_fields=['total_points', 'updated_at'])

    # Award any newly eligible badges.
    award_eligible_badges(student, student_points.total_points)

    return transaction_record


def award_eligible_badges(student, total_points):
    eligible_badges = Badge.objects.filter(
        is_active=True,
        points_required__lte=total_points
    ).exclude(
        recipients__student=student
    )

    for badge in eligible_badges:
        StudentBadge.objects.get_or_create( student=student, badge=badge )


@transaction.atomic
def update_learning_streak(student):
    today = timezone.localdate()

    streak, _ = LearningStreak.objects.get_or_create(
        student=student
    )

    streak = LearningStreak.objects.select_for_update().get(
        id=streak.id
    )

    last_date = streak.last_activity_date

    # Multiple activities on the same day do not increase the streak.
    if last_date == today:
        return streak

    if last_date is None:
        streak.current_streak = 1

    elif (today - last_date).days == 1:
        streak.current_streak += 1

    else:
        # The student missed at least one day.
        streak.current_streak = 1

    streak.longest_streak = max(
        streak.longest_streak,
        streak.current_streak
    )

    streak.last_activity_date = today

    streak.save()

    # Give a bonus every 7 consecutive learning days.
    if streak.current_streak > 0 and streak.current_streak % 7 == 0:

        award_points(
            student=student,
            activity_type=PointTransaction.ActivityType.STREAK,
            points=50,
            description=(
                f"Maintained a {streak.current_streak}-day learning streak"
            ),
            source_id=today.isoformat()
        )

    return streak