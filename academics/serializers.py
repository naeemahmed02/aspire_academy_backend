from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Subject, MainTopic, SubTopic


# SubTopic Serializers

class SubTopicWriteSerializer(serializers.ModelSerializer):
    """
    Serializer used for create/update operations.
    Ensures a sub-topic name is unique within a main topic.
    """

    class Meta:
        model = SubTopic
        fields = [
            "id",
            "main_topic",
            "sub_topic_name",
            "sub_topic_description",
        ]
        read_only_fields = ["id"]

        validators = [
            UniqueTogetherValidator(
                queryset=SubTopic.objects.all(),
                fields=["main_topic", "sub_topic_name"],
                message="This sub-topic already exists for this main topic."
            )
        ]

    def validate_sub_topic_name(self, value):
        """
        Normalize input to avoid duplicates like:
        'Neural Networks', 'neural networks', 'Neural Networks '
        """
        return value.strip()


class SubTopicReadSerializer(serializers.ModelSerializer):
    """
    Serializer used for detailed read operations.
    """

    class Meta:
        model = SubTopic
        fields = [
            "id",
            "sub_topic_name",
            "sub_topic_description",
        ]


class SubTopicListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for dropdowns or lists.
    """

    class Meta:
        model = SubTopic
        fields = [
            "id",
            "sub_topic_name",
        ]


# MainTopic Serializers


class MainTopicWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for create/update operations on MainTopic.
    Ensures uniqueness within a subject.
    """

    class Meta:
        model = MainTopic
        fields = [
            "id",
            "subject",
            "topic_name",
            "topic_description",
        ]
        read_only_fields = ["id"]

        validators = [
            UniqueTogetherValidator(
                queryset=MainTopic.objects.all(),
                fields=["subject", "topic_name"],
                message="This topic already exists for this subject."
            )
        ]

    def validate_topic_name(self, value):
        return value.strip()


class MainTopicReadSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed topic view including subtopics.
    """

    sub_topics = SubTopicReadSerializer(many=True, read_only=True)

    class Meta:
        model = MainTopic
        fields = [
            "id",
            "topic_name",
            "topic_description",
            "sub_topics",
        ]


class MainTopicListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for lists or dropdowns.
    """

    class Meta:
        model = MainTopic
        fields = [
            "id",
            "topic_name",
        ]


# Subject Serializers


class SubjectWriteSerializer(serializers.ModelSerializer):
    """
    Serializer used for create/update subject operations.
    Ensures subject name is unique (case insensitive).
    """

    class Meta:
        model = Subject
        fields = [
            "id",
            "subject_name",
            "subject_code",
            "subject_description",
        ]
        read_only_fields = ["id"]

    def validate_subject_name(self, value):
        """
        Prevent duplicate subject names.
        Case-insensitive validation.
        """
        value = value.strip()

        queryset = Subject.objects.filter(subject_name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A subject with this name already exists."
            )

        return value


class SubjectReadSerializer(serializers.ModelSerializer):
    """
    Detailed serializer including nested topics.
    """

    main_topics = MainTopicReadSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = [
            "id",
            "subject_name",
            "subject_code",
            "subject_description",
            "main_topics",
        ]


class SubjectListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for dropdowns or lists.
    """

    class Meta:
        model = Subject
        fields = [
            "id",
            "subject_name",
        ]