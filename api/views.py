from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from core.models import Game
from utils.words import words, get_random_word
from utils.play import check_if_won, check_if_lost, verify_guess

from api.serializer import GameSerializer


class Start(APIView):
    def post(self, request):
        MAX_GUESSES = 8
        difficulty = request.data.pop('difficulty', None)

        if difficulty is None:
            message = {'difficulty': 'Please provide a value for difficulty'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        difficulty = difficulty.upper()

        if difficulty in ['E', 'M', 'H']:
            if difficulty == 'M':
                MAX_GUESSES -= 2
            if difficulty == 'H':
                MAX_GUESSES -= 4

            secret_word, secret_set = get_random_word(words)
            game = Game.objects.create(
                difficulty=difficulty,
                secret_word=secret_word,
                secret_set=secret_set,
                max_guesses=MAX_GUESSES
            )
            data = GameSerializer(game).data
            data.pop('secret_word')
            return Response(data, status=status.HTTP_200_OK)
        else:
            message = {'difficulty': 'Invalid value set for difficulty. E - Easy, M - Medium, H - Hard'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class GetState(APIView):
    def post(self, request):
        id = request.data.pop('id', None)

        if id is None:
            message = {'id': 'Please provide a value for id'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            game = Game.objects.get(id=id)
            data = GameSerializer(game).data
            if not game.is_done:
                data.pop('secret_word')

            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            message = {'id': 'Game with provided id does not exist'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)


class Guess(APIView):
    def post(self, request):
        id = request.data.pop('id', None)
        guess = request.data.pop('guess', None)

        message = {}
        if id is None:
            message['id'] = 'Please provide a value for id'
        if guess is None:
            message['guess'] = 'Please provide a value for guess'

        if message:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            guess = guess.lower()
            game = Game.objects.get(id=id)
            secret_word = game.secret_word
            missed_letters = game.missed_letters
            correct_letters = game.correct_letters
            max_guesses = game.max_guesses
            already_guessed = missed_letters + correct_letters

            if game.is_done:
                message = {'message': 'Game is over'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            message = verify_guess(guess, already_guessed)
            if message:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            if guess in secret_word:
                correct_letters += guess
                if check_if_won(correct_letters, secret_word):
                    game.is_done = True
                    game.result = 'W'
            else:
                missed_letters += guess
                if check_if_lost(missed_letters, max_guesses):
                    game.is_done = True
                    game.result = 'L'

            game.missed_letters = missed_letters
            game.correct_letters = correct_letters
            game.save()

            data = GameSerializer(game).data
            if not game.is_done:
                data.pop('secret_word')

            return Response(data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            message = {'id': 'Game with provided id does not exist'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
