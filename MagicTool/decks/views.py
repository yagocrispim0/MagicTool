from django.shortcuts import render

# Create your views here.
def create_deck(request):
    return render(request, 'decks/create_deck.html')