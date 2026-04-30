from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StudentProgressSummaryViewSet,
    StudentDashboardAPIView,
)

router = DefaultRouter()

router.register(
    r'progress',
    StudentProgressSummaryViewSet,
    basename='progress'
)

urlpatterns = [
    path(
        "student-dashboard/",
        StudentDashboardAPIView.as_view(),
        name="student-dashboard"
    ),

    path(
        "",
        include(router.urls)
    ),
]