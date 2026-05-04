from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404

from courses.models import (
    Course,
    Video,
    VideoProgress
)

from .serializers import (
    CourseSerializer,
    VideoProgressSerializer
)

from courses.services.access_service import (
    user_has_course_access
)



class CourseDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        course = get_object_or_404(
            Course,
            id=course_id,
            is_published=True
        )

        has_access = user_has_course_access(
            request.user,
            course
        )

        if not has_access:
            return Response(
                {
                    "detail": "You do not have access to this course."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CourseSerializer(course)

        return Response(serializer.data)

class UpdateVideoProgressAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        video_id = request.data.get("video_id")
        watched_seconds = request.data.get("watched_seconds", 0)
        completed = request.data.get("completed", False)

        video = get_object_or_404(Video, id=video_id)

        course = video.playlist.course

        has_access = user_has_course_access(
            request.user,
            course
        )

        if not has_access:
            return Response(
                {
                    "detail": "Access denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        progress, _ = VideoProgress.objects.update_or_create(
            user=request.user,
            video=video,
            defaults={
                "watched_seconds": watched_seconds,
                "completed": completed,
            }
        )

        serializer = VideoProgressSerializer(progress)

        return Response(serializer.data)

class MyCoursesAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        courses = Course.objects.filter(
            enrollments__user=request.user,
            enrollments__is_active=True,
            is_published=True
        ).distinct()

        serializer = CourseSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)