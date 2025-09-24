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
    cards = models.ManyToManyField('Card')

    def __str__(self):
        return self.name


class Card(models.Model):
    scryfall_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name