from rest_framework import viewsets
from announcement.models import Announcement
from .serializers import AnnouncementSerializer
from announcement.permissions.permissions import AnnouncementPermission

class AnnouncementViewSet(viewsets.ModelViewSet):
    permission_classes = [AnnouncementPermission]
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer