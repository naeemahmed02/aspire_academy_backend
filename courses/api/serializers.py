from rest_framework import serializers

from courses.models import (
    Course,
    Playlist,
    Video,
    VideoProgress
)


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "youtube_video_id",
            "duration_seconds",
            "order",
            "is_preview",
        ]


class PlaylistSerializer(serializers.ModelSerializer):

    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = [
            "id",
            "title",
            "order",
            "videos",
        ]


class CourseSerializer(serializers.ModelSerializer):

    playlists = PlaylistSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "thumbnail",
            "playlists",
        ]


class VideoProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoProgress
        fields = [
            "video",
            "watched_seconds",
            "completed",
        ]