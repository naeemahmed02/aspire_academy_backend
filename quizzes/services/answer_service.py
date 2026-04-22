from quizzes.models import StudentAnswer


class AnswerService:

    @staticmethod
    def submit_answer(attempt, question, selected_option, time_taken):
        """
        Production safe answer submission
        """

        # Prevent duplicate
        if StudentAnswer.objects.filter(
            quiz_attempt=attempt,
            question=question
        ).exists():
            return None, "Already answered"

        # Validate question belongs to attempt
        if not attempt.questions.filter(id=question.id).exists():
            return None, "Invalid question"

        is_correct = (selected_option == question.correct_answer)

        marks = 1 if is_correct else 0

        answer = StudentAnswer.objects.create(
            quiz_attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            marks_awarded=marks,
            time_taken=time_taken,
        )

        return answer, None