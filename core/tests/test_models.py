from django.test import TestCase
from core.models import Game
from utils.words import get_random_word, words
from utils.play import write_board


class GameModelTests(TestCase):
    """Test class for the Game model"""

    def test_game_str(self):
        """Test the game model string representation"""
        secret_word, secret_set = get_random_word(words)
        game = Game.objects.create(
            difficulty='E',
            secret_word=secret_word,
            secret_set=secret_set,
            max_guesses=8,
            board=write_board("", secret_word)
        )

        self.assertEqual(str(game), game.id)
