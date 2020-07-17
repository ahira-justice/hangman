from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from core.models import Game
from utils.words import words, get_random_word
from api.serializer import GameSerializer, GuessSerializer


class Start(APIView):
    def post(self, request):
        difficulty = request.data['difficulty']

        if difficulty.upper() in ['E', 'M', 'H']:
            secret_word, secret_set = get_random_word(words)
            game = Game.objects.create(
                difficulty=difficulty,
                secret_word=secret_word,
                secret_set=secret_set,
            )
            data = GameSerializer(game).data
            data.pop('secret_word')
            return Response(data, status=status.HTTP_200_OK)

        message = {'difficulty': 'Invalid value set for difficulty. E - Easy, M - Medium, H - Hard'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class GetState(APIView):
    def post(self, request):
        try:
            game = Game.objects.get(id=request.data['id'])
            data = GameSerializer(game).data
            data.pop('secret_word')
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            message = {'id': 'Game with provided id does not exist'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
