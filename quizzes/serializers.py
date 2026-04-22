# from rest_framework import serializers
# from .models import QuizAttempt, StudentAnswer


# # =========================================================
# # 🔹 STUDENT ANSWER SERIALIZERS
# # =========================================================

# class StudentAnswerWriteSerializer(serializers.ModelSerializer):
#     """
#     Submit answer serializer (production safe)
#     """

#     class Meta:
#         model = StudentAnswer
#         fields = [
#             "question",
#             "selected_option",
#             "time_taken",
#         ]

#     def validate(self, attrs):
#         request = self.context.get("request")
#         attempt = self.context.get("attempt")

#         question = attrs["question"]

#         # 🔒 Ensure attempt exists
#         if not attempt:
#             raise serializers.ValidationError("Invalid attempt")

#         # 🔒 Check ownership
#         if attempt.student != request.user:
#             raise serializers.ValidationError("Not allowed")

#         # 🔒 Check quiz status
#         if attempt.status != "IN_PROGRESS":
#             raise serializers.ValidationError("Quiz already completed")

#         # 🔒 Ensure question belongs to this attempt
#         if not attempt.questions.filter(id=question.id).exists():
#             raise serializers.ValidationError("Invalid question for this attempt")

#         # 🔒 Prevent duplicate answer
#         if StudentAnswer.objects.filter(
#             quiz_attempt=attempt,
#             question=question
#         ).exists():
#             raise serializers.ValidationError("Already answered")

#         return attrs


# class StudentAnswerReadSerializer(serializers.ModelSerializer):
#     question_text = serializers.CharField(
#         source="question.question_text",
#         read_only=True
#     )

#     class Meta:
#         model = StudentAnswer
#         fields = [
#             "id",
#             "question",
#             "question_text",
#             "selected_option",
#             "is_correct",
#             "marks_awarded",
#             "time_taken",
#             "answered_at",
#         ]


# # =========================================================
# # 🔹 QUIZ ATTEMPT SERIALIZERS
# # =========================================================

# class QuizAttemptCreateSerializer(serializers.ModelSerializer):
#     """
#     Start quiz
#     """
#     sub_topic_name = serializers.CharField(
#         source="sub_topic.sub_topic_name",
#         read_only=True
#     )

#     class Meta:
#         model = QuizAttempt
#         fields = [
#             "id",
#             "sub_topic",
#             'sub_topic_name',
#             "total_questions",
#             "time_limit",
#         ]
#         read_only_fields = ["id"]

#     # def create(self, validated_data):
#     #     user = self.context["request"].user

#     #     return QuizAttempt.objects.create(
#     #         student=user,
#     #         **validated_data
#     #     )


# class QuizAttemptListSerializer(serializers.ModelSerializer):
#     sub_topic_name = serializers.CharField(
#         source="sub_topic.sub_topic_name",
#         read_only=True
#     )

#     duration_taken = serializers.SerializerMethodField()

#     class Meta:
#         model = QuizAttempt
#         fields = [
#             "id",
#             "sub_topic_name",
#             "score",
#             "accuracy",
#             "status",
#             "started_at",
#             "completed_at",
#             "duration_taken",
#         ]

#     def get_duration_taken(self, obj):
#         if obj.completed_at:
#             return (obj.completed_at - obj.started_at).seconds
#         return None


# class QuizAttemptDetailSerializer(serializers.ModelSerializer):
#     answers = StudentAnswerReadSerializer(many=True, read_only=True)

#     sub_topic_name = serializers.CharField(
#         source="sub_topic.sub_topic_name",
#         read_only=True
#     )

#     duration_taken = serializers.SerializerMethodField()

#     class Meta:
#         model = QuizAttempt
#         fields = [
#             "id",
#             "sub_topic",
#             "sub_topic_name",
#             "total_questions",
#             "time_limit",

#             "started_at",
#             "completed_at",

#             "score",
#             "correct_answers",
#             "wrong_answers",
#             "skipped_questions",
#             "accuracy",
#             "status",

#             "duration_taken",
#             "answers",
#         ]

#     def get_duration_taken(self, obj):
#         if obj.completed_at:
#             return (obj.completed_at - obj.started_at).seconds
#         return None






from rest_framework import serializers
from .models import QuizAttempt, StudentAnswer



# STUDENT ANSWER (WRITE)
class StudentAnswerWriteSerializer(serializers.ModelSerializer):
    """
    ONLY validates input structure.
    Business rules are handled in service layer.
    """

    class Meta:
        model = StudentAnswer
        fields = [
            "question",
            "selected_option",
            "time_taken",
        ]

    def validate(self, attrs):
        # basic null safety only (NO business logic here)
        if not attrs.get("question"):
            raise serializers.ValidationError("Question is required")

        if not attrs.get("selected_option"):
            raise serializers.ValidationError("Selected option is required")

        return attrs



# STUDENT ANSWER (READ)
class StudentAnswerReadSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(
        source="question.question_text",
        read_only=True
    )

    class Meta:
        model = StudentAnswer
        fields = [
            "id",
            "question",
            "question_text",
            "selected_option",
            "is_correct",
            "marks_awarded",
            "time_taken",
            "answered_at",
        ]


# QUIZ ATTEMPT (CREATE)
class QuizAttemptCreateSerializer(serializers.ModelSerializer):
    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "sub_topic",
            "sub_topic_name",
            "total_questions",
            "time_limit",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context["request"]

        # FIX: always assign student
        return QuizAttempt.objects.create(
            **validated_data
        )


# QUIZ ATTEMPT (LIST)
class QuizAttemptListSerializer(serializers.ModelSerializer):
    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    duration_taken = serializers.SerializerMethodField()

    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "sub_topic_name",
            "score",
            "accuracy",
            "status",
            "started_at",
            "completed_at",
            "duration_taken",
        ]

    def get_duration_taken(self, obj):
        if obj.completed_at and obj.started_at:
            return (obj.completed_at - obj.started_at).seconds
        return 0



# QUIZ ATTEMPT (DETAIL)

class QuizAttemptDetailSerializer(serializers.ModelSerializer):
    answers = StudentAnswerReadSerializer(many=True, read_only=True)

    sub_topic_name = serializers.CharField(
        source="sub_topic.sub_topic_name",
        read_only=True
    )

    duration_taken = serializers.SerializerMethodField()

    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "sub_topic",
            "sub_topic_name",
            "total_questions",
            "time_limit",

            "started_at",
            "completed_at",

            "score",
            "correct_answers",
            "wrong_answers",
            "skipped_questions",
            "accuracy",
            "status",

            "duration_taken",
            "answers",
        ]

    def get_duration_taken(self, obj):
        if obj.completed_at and obj.started_at:
            return (obj.completed_at - obj.started_at).seconds
        return 0