from rest_framework import serializers
from django.db import IntegrityError
from .models import Subject, MainTopic, SubTopic


# SubTopic Serializers

class SubTopicWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic

        fields = [
            'id',
            'main_topic',
            'sub_topic_name',
            'sub_topic_description',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        main_topic = attrs.get("main_topic")
        name = attrs.get("sub_topic_name")

        if SubTopic.objects.filter(
            main_topic = main_topic,
            sub_topic = name
        ).exists():
            raise serializers.ValidationError(
                {"sub_topic_name": "This sub-topic already exists for this main topic."}
            )
        
        return attrs
    
class SubTopicReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = [
            "id",
            "sub_topic_name",
            "sub_topic_description",
        ]

class SubTopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopic
        fields = ["id", "sub_topic_name"]


# MainTopic Serializers

class MainTopicWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTopic
        fields = [
            "id",
            "subject",
            "topic_name",
            "topic_description",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        subject = attrs.get("subject")
        name = attrs.get("topic_name")

        if MainTopic.objects.filter(
            subject= subject,
            topic_name = name
        ).exists():
            raise serializers.ValidationError(
                {"topic_name": "This topic already exists for this subject."}
            )
        return attrs
    
class MainTopicReadSerialzier(serializers.ModelSerializer):
    sub_topics = SubTopicReadSerializer(manay = True, read_only=True)

    class Meta:
        model = MainTopic
        fields = [
            "id",
            "topic_name",
            "topic_description",
            "sub_topics",
        ]


class MainTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTopic
        fields = ["id", "topic_name"]


# Subject Serializers

class SubjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "subject_name",
            "subject_code",
            "subject_description"
        ]
        read_only_fields = ["id"]

    def validate_subject_name(self, value):
        if Subject.objects.filter(subject_name=value).exists():
            raise serializers.ValidationError(
                "A subject with this name already exists."
            )
        return value