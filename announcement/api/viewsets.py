from rest_framework import viewsets
from .models import Announcement
from .serializers import AnnouncementSerializer
from rest_framework.permissions import IsAdminUser

class AnnouncementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer