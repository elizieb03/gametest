from django.db import models
from django.contrib.auth.models import User
from .funcs import generateNumber

class EmailCode(models.Model):
    code = models.CharField(max_length=50, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.id:
            self.code = generateNumber()
        return super(EmailCode, self).save(*args, **kwargs)

class Quiz(models.Model):
    subject = models.CharField(max_length=50)
    difficulty = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.subject + " - " + str(self.difficulty)

class Question(models.Model):
    title = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def get_correct_answer(self):
        return self.answers.filter(correct=True).first()
    def check_correct_answers(self, answer_id):
        return self.answers.filter(id=answer_id, correct=True).exists()
    def __str__(self):
        return self.title

class Answer(models.Model):
    title = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    correct = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id) + " - " + self.title + " - " + self.question.title

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    result = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.get_full_name() + " - " + self.quiz.subject
