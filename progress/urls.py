from rest_framework.routers import DefaultRouter
from .views import (
    StudentProgressSummaryViewSet,
    StudentProgressHistoryViewSet
)

router = DefaultRouter()

router.register(
    "progress",
    StudentProgressSummaryViewSet,
    basename="progress"
)

router.register(
    "progress-history",
    StudentProgressHistoryViewSet,
    basename="progress-history"
)

urlpatterns = router.urls