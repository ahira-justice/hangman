from django.db import models

from utils.rstring import make_id
from utils.difficulty import DIFFICULTY_CHOICES


class Game(models.Model):
    id = models.CharField(primary_key=True, default=make_id, editable=False, max_length=5)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    missed_letters = models.CharField(max_length=255, blank=True)
    correct_letters = models.CharField(max_length=255, blank=True)
    max_guesses = models.IntegerField()
    secret_word = models.CharField(max_length=255)
    secret_set = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    result = models.CharField(max_length=1, blank=True)
