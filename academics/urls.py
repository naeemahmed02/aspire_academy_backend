from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, MainTopicViewSet, SubTopicViewSet

router = DefaultRouter()

router.register("subjects", SubjectViewSet)
router.register("main-topics", MainTopicViewSet)
router.register("sub-topics", SubTopicViewSet)

urlpatterns = router.urls