from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', "first_name", "last_name"]
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class GameSerializer(serializers.ModelSerializer):
    answers = serializers.JSONField(required=False)
    class Meta:
        model = Game
        fields = ['user', 'id', 'quiz', 'result', 'answers']
        extra_kwargs = {
            'user': {'read_only': True},
            'quiz': {'read_only': True}
        }
    def validate_answers(self, value):
        questions = [obj['question'] for obj in value]
        count_quiz_questions = self.context['quiz'].questions.filter(id__in=questions).count()
        if count_quiz_questions != len(questions):
            raise serializers.ValidationError('Respostas invalidas')
        
        return value
    
    def create(self, validated_data):
        user = self.context['user']
        quiz = self.context['quiz']
        game = Game(user=user, quiz=quiz)
        answers = validated_data.pop('answers')
        count = 0
        for answer in answers:
            question = Question.objects.get(id=answer['question'])
            if question.check_correct_answers(answer['answer']):
                count += 1
        game.result = count
        game.save()
        return game  

class EmailCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCode
        fields = ['date']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'title']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = ['id', 'title', 'answers']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'subject', 'difficulty', 'description']

class QuizDetailsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Quiz
        fields = ['id', 'subject', 'difficulty', 'description', 'questions']