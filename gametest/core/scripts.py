from core.models import Quiz, Question, Answer
from django.db import transaction

@transaction.atomic
def create_quiz(subject, difficulty, description, questions):
    quiz = Quiz.objects.create(subject=subject, difficulty=difficulty, description=description)

    for question in questions:
        answers = question.pop('answers')
        question_object = Question.objects.create(**question, quiz_id=quiz.id)
        for answer in answers:
          Answer.objects.create(**answer, question_id=question_object.id)
