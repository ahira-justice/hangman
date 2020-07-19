from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Game
from api.serializer import GameSerializer


START_URL = reverse('api:start')
STATE_URL = reverse('api:state')
GUESS_URL = reverse('api:guess')


class StartApiTests(TestCase):
    """Test class for the start API"""

    def setUp(self):
        self.client = APIClient()

    def test_start_difficulty_not_provided(self):
        res = self.client.post(START_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_invalid_difficulty(self):
        payload = {
            'difficulty': 'EASY'
        }
        res = self.client.post(START_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_valid_difficulty(self):
        game_count = Game.objects.all().count()
        payload = {
            'difficulty': 'E'
        }
        res = self.client.post(START_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(game_count + 1, Game.objects.all().count())
        self.assertIn('id', res.data)


class StateApiTests(TestCase):
    """Test class for the state API"""

    def setUp(self):
        self.client = APIClient()

    def test_state_id_not_provided(self):
        res = self.client.post(STATE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_state_invalid_id(self):
        payload = {
            'id': 'DxjJZ'
        }
        res = self.client.post(STATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_state_valid_id(self):
        game = Game.objects.create(
            difficulty='E',
            secret_word='word',
            secret_set='set',
            max_guesses=4,
            board='____'
        )

        payload = {
            'id': game.id
        }
        res = self.client.post(STATE_URL, payload)
        data = GameSerializer(game).data
        data.pop('secret_word')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, data)


class GuessApiTests(TestCase):
    """Test class for the guess API"""

    def setUp(self):
        self.client = APIClient()

    def test_guess_id_not_provided(self):
        payload = {
            'guess': 'w'
        }
        res = self.client.post(GUESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guess_guess_not_provided(self):
        payload = {
            'id': 'DxjJZ'
        }
        res = self.client.post(GUESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guess_game_is_done(self):
        game = Game.objects.create(
            difficulty='E',
            secret_word='word',
            secret_set='set',
            max_guesses=4,
            board='____',
            is_done=True
        )

        payload = {
            'id': game.id,
            'guess': 'w'
        }
        res = self.client.post(GUESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guess_invalid_id(self):
        payload = {
            'id': 'DxjJZ',
            'guess': 'w'
        }
        res = self.client.post(GUESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_guess_invalid_guess(self):
        game = Game.objects.create(
            difficulty='E',
            secret_word='word',
            secret_set='set',
            max_guesses=4,
            board='____'
        )

        payload = {
            'id': game.id,
            'guess': 'word'
        }
        res = self.client.post(GUESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guess_valid(self):
        game = Game.objects.create(
            difficulty='E',
            secret_word='word',
            secret_set='set',
            max_guesses=4,
            board='____'
        )

        payload = {
            'id': game.id,
            'guess': 'w'
        }
        res = self.client.post(GUESS_URL, payload)
        game.refresh_from_db()
        data = GameSerializer(game).data
        data.pop('secret_word')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, data)
        self.assertIn(payload['guess'], data['correct_letters'])
