from django.utils import timezone

from courses.models import Enrollment


def user_has_course_access(user, course):

    enrollment = Enrollment.objects.filter(
        user=user,
        course=course,
        is_active=True
    ).first()

    if not enrollment:
        return False

    if enrollment.expires_at:
        if enrollment.expires_at < timezone.now():
            return False

    return True