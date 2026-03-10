from rest_framework.routers import DefaultRouter
from .views import QuizAttemptViewSet

router = DefaultRouter()
router.register("quiz-attempts", QuizAttemptViewSet, basename="quiz")

urlpatterns = router.urls