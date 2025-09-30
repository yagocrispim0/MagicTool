import uuid
from django.db import models



class Deck(models.Model):
    # Defines format choices for the deck
    class FormatChoices(models.TextChoices):
        STANDARD = 'STD', 'Standard'
        MODERN = 'MOD', 'Modern'
        LEGACY = 'LGC', 'Legacy'
        VINTAGE = 'VIN', 'Vintage'
        COMMANDER = 'EDH', 'Commander'
        PAUPER = 'PPR', 'Pauper'
        NONE = 'NON', 'Sem Formato'

    name = models.CharField(max_length=200)
    format = models.CharField(max_length=3, choices=FormatChoices.choices, default=FormatChoices.NONE)
    cards = models.ManyToManyField('Card', through='DeckCard', related_name='decks')    

    def __str__(self):
        return self.name

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Card(models.Model):
    scryfall_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name