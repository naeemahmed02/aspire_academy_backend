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
    main_topic = serializers.IntegerField(source="main_topic.id", read_only=True)
    main_topic_name = serializers.CharField(source="main_topic.topic_name", read_only=True)

    class Meta:
        model = SubTopic
        fields = [
            "id",
            "sub_topic_name",
            "main_topic",
            "main_topic_name",
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
    subject = serializers.IntegerField(source="subject.id", read_only=True)
    subject_name = serializers.CharField(source="subject.subject_name", read_only=True)

    class Meta:
        model = MainTopic
        fields = [
            "id",
            "topic_name",
            "subject",
            "subject_name",
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
            "sub_image",
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

    sub_image = serializers.SerializerMethodField()

    def get_sub_image(self, obj):
        request = self.context.get("request")
        if obj.sub_image:
            if request:
                return request.build_absolute_uri(obj.sub_image.url)
            return obj.sub_image.url
        return None

    main_topics = MainTopicReadSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = [
            "id",
            "subject_name",
            "subject_code",
            "subject_description",
            "main_topics",
            "sub_image",
        ]


class SubjectListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for dropdowns or lists.
    """

    def get_sub_image(self, obj):
        request = self.context.get("request")
        if obj.sub_image:
            if request:
                return request.build_absolute_uri(obj.sub_image.url)
            return obj.sub_image.url
        return None

    class Meta:
        model = Subject
        fields = [
            "id",
            "subject_name",
            'sub_image'
        ]