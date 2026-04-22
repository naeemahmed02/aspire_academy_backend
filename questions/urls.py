from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, QuestionReadSerializer

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="questions")
# router.register("questions", QuestionReadSerializer, basename="questions")

urlpatterns = router.urls