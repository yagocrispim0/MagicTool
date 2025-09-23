from django.db import models


class Deck(models.Model):
    name = models.CharField(max_length=200)
    cards = models.ManyToManyField(Card)

    def __str__(self):
        return self.name


class Card(models.Model):
    scryfall_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name