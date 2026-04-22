# quizzes/services/scoring_service.py

class ScoringService:

    @staticmethod
    def calculate(attempt):
        """
        Calculate final quiz result
        """

        answers = attempt.answers.all()

        correct = answers.filter(is_correct=True).count()
        wrong = answers.filter(is_correct=False).count()
        total_answered = answers.count()

        skipped = attempt.total_questions - total_answered

        score = sum(a.marks_awarded for a in answers)

        accuracy = 0
        if total_answered > 0:
            accuracy = (correct / total_answered) * 100

        return {
            "correct": correct,
            "wrong": wrong,
            "skipped": skipped,
            "score": score,
            "accuracy": accuracy
        }

    @staticmethod
    def apply(attempt, result):
        """
        Save computed result into DB
        """

        attempt.correct_answers = result["correct"]
        attempt.wrong_answers = result["wrong"]
        attempt.skipped_questions = result["skipped"]
        attempt.score = result["score"]
        attempt.accuracy = result["accuracy"]

        attempt.save()

        return attempt