from rest_framework import permissions
from core.serializers import *
from core.models import *
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import permissions, authentication, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Create your views user.
class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, resquest, *args, **kwargs):
        return Response(self.serializer_class(resquest.user).data)

class UpdateDeleteUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuizView(generics.ListAPIView):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

class GameView(generics.CreateAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = {
            'user': self.request.user,
            'quiz': Quiz.objects.get(id=self.kwargs['id'])
        }
        return context

class CheckAnswersView(APIView):
    def post(self, request, **kwargs):
        question = get_object_or_404(Question, id=kwargs['question_id'], quiz=kwargs['quiz_id'])
        result = question.check_correct_answers(request.data['answer'])
        correct_answers = getattr(question.get_correct_answer(), 'title', None)

        return Response({'result': result, 'correct_answers': correct_answers})
    
class GamePlayView(generics.UpdateAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

class QuizDetailView(generics.RetrieveAPIView):
    serializer_class = QuizDetailsSerializer
    queryset = Quiz.objects.all()
    lookup_field = 'id'
