from django.urls import path

from .views import (
    CourseDetailAPIView,
    UpdateVideoProgressAPIView,
    MyCoursesAPIView
)

urlpatterns = [

    path(
        "my-courses/",
        MyCoursesAPIView.as_view(),
        name="my-courses"
    ),

    path(
        "course/<int:course_id>/",
        CourseDetailAPIView.as_view(),
        name="course-detail"
    ),

    path(
        "video-progress/",
        UpdateVideoProgressAPIView.as_view(),
        name="video-progress"
    ),
]