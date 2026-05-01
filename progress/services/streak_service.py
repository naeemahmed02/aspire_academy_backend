from datetime import date, timedelta
from ..models import UserActivityEvent


def get_user_activity_dates(user):
    events = UserActivityEvent.objects.filter(
        user=user,
        event_type="QUIZ_ATTEMPT"
    )

    return list(
        set([e.created_at.date() for e in events])
    )


def calculate_streak(activity_dates):
    dates = sorted(set(activity_dates), reverse=True)

    today = date.today()

    streak = 0

    for i in range(len(dates)):
        expected_date = today - timedelta(days=i)

        if dates[i] == expected_date:
            streak += 1
        else:
            break

    return streak


def update_user_streak(user):

    # 1. Save activity event
    UserActivityEvent.objects.create(
        user=user,
        event_type="QUIZ_ATTEMPT"
    )

    # 2. Get unique activity dates
    dates = get_user_activity_dates(user)

    # 3. Calculate streak
    streak = calculate_streak(dates)

    # 4. Update cache fields
    user.current_streak = streak

    if streak > user.max_streak:
        user.max_streak = streak

    user.save()

    return streak