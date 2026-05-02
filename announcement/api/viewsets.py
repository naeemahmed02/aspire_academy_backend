from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from announcement.models import Announcement
from .serializers import AnnouncementSerializer
from announcement.permissions.permissions import (
    IsTeacherOrAdmin,
    IsAuthenticatedReadOnly,
)

import logging

logger = logging.getLogger(__name__)


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer

    def get_permissions(self):

        logger.info(f"ACTION: {self.action}")
        logger.info(f"USER: {self.request.user}")
        logger.info(f"AUTH: {self.request.user.is_authenticated}")
        """
        Assign permissions based on action
        """
        if self.action in ['list', 'retrieve']:
            # Anyone logged in can read
            return [IsAuthenticated()]

        # Only teachers/admins can modify
        return [IsTeacherOrAdmin()]
