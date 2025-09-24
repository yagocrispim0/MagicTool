from django.shortcuts import render, redirect
from .models import Deck

# Create your views here.
def create_deck(request):

    if request.method == 'POST':
        deck_name = request.POST.get('deck_name')
        deck_format = request.POST.get('deck_format')

        Deck.objects.create(name=deck_name, format=deck_format)

        return  redirect('decks_list')
    
    return render(request, 'decks/create_deck.html')


def decks_list(request):

    all_decks = Deck.objects.order_by('name')
    context = {'decks': all_decks}
    return render(request, 'decks/decks_list.html', context)