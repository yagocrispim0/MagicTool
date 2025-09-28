import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Deck, Card


def edit_deck(request, deck_id):

    deck = get_object_or_404(Deck, id=deck_id)

    if request.method == 'POST':
        deck_name = request.POST.get('deck_name')
        deck_format = request.POST.get('deck_format')
        deck.name = deck_name
        deck.format = deck_format
        deck.save()

        card_list_str = request.POST.get('card_list', '')
        deck.cards.clear()
        if card_list_str:
            card_names = card_list_str.split('||')
            for name in card_names:
                card_obj, created = Card.objects.get_or_create(name=name.strip())
                deck.cards.add(card_obj)
        return redirect ('deck_detail', deck_id=deck.id)

    context = {'deck': deck,
               'formats': Deck.FormatChoices.choices}
    return render(request, 'decks/edit_deck.html', context)



def deck_detail(request, deck_id):

    deck = get_object_or_404(Deck, id=deck_id)
    
    if request.method == 'POST':
        deck.delete()
        return redirect('decks_list')

    context = {'deck': deck}
    return render(request, 'decks/deck_detail.html', context)

# Adiciona um novo deck ao banco de dados
def create_deck(request):

    if request.method == 'POST':
        deck_name = request.POST.get('deck_name')
        deck_format = request.POST.get('deck_format')
        new_deck = Deck.objects.create(name=deck_name, format=deck_format)
        #Pega a lista de cartas do input hidden
        card_list_str = request.POST.get('card_list', '')

        if card_list_str:
            card_names = card_list_str.split('||')
            for name in card_names:
                card_obj, created = Card.objects.get_or_create(name=name.strip())
                new_deck.cards.add(card_obj)
        return  redirect('deck_detail', deck_id=new_deck.id)
    
    return render(request, 'decks/create_deck.html')

# Lista todos os decks no banco de dados
def decks_list(request):

    all_decks = Deck.objects.order_by('name')
    context = {'decks': all_decks}
    return render(request, 'decks/decks_list.html', context)

# Autocompletar nomes de cartas usando a API Scryfall
def card_autocomplete(request):
    
    query = request.GET.get('card', '')

    if len(query) > 1:
        scryfall_url = f"https://api.scryfall.com/cards/autocomplete?q={query}"
        try:
            response = requests.get(scryfall_url)
            response.raise_for_status()
            data = response.json()
            card_names = data.get('data', [])
            return JsonResponse(card_names, safe=False)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse([], safe=False)