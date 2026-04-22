from rest_framework.routers import DefaultRouter
from .views import (
    StudentProgressSummaryViewSet
)

router = DefaultRouter()

router.register(
    "progress",
    StudentProgressSummaryViewSet,
    basename="progress"
)

urlpatterns = router.urls