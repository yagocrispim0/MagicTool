import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from .models import Deck, Card, DeckCard
from .forms import DeckForm

# Edita um deck existente
@never_cache
def edit_deck(request, deck_id):

    deck = get_object_or_404(Deck, id=deck_id)

    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)

        if form.is_valid():
            deck = form.save()

            card_list_str = request.POST.get('card_list', '')
            deck.cards.clear()
            if card_list_str:
                card_names = card_list_str.split('||')
                for name in card_names:
                    card_obj, created = Card.objects.get_or_create(name=name.strip())
                    deck.cards.add(card_obj)
            return redirect ('deck_detail', deck_id=deck.id)

    else:
        form = DeckForm(instance=deck)

    context = {'form': form, 
               'deck': deck,}
    return render(request, 'decks/edit_deck.html', context)



def deck_detail(request, deck_id):

    deck = get_object_or_404(Deck, id=deck_id)
    
    if request.method == 'POST':
        deck.delete()
        return redirect('decks_list')

    context = {'deck': deck}
    return render(request, 'decks/deck_detail.html', context)

# Adiciona um novo deck ao banco de dados
@never_cache
def create_deck(request):

    if request.method == 'POST':
        form = DeckForm(request.POST)

        if form.is_valid():
            deck = form.save()

            card_list_str = request.POST.get('card_list', '')
            if card_list_str:
                cardsInfo = card_list_str.split(';;')
                for cardInfo in cardsInfo:
                    if len(cardInfo.split('||')) == 2:
                        quantityStr, name = cardInfo.split('||')
                        try:
                            quantity = int(quantityStr.strip())
                            card_obj, created = Card.objects.get_or_create(name=name.strip())
                            DeckCard.objects.create(deck=deck, card=card_obj, quantity=quantity)
                        except ValueError:
                            continue

            return redirect ('deck_detail', deck_id=deck.id)
    else:
        form = DeckForm()

    context = {'form': form}

    return render(request, 'decks/create_deck.html', context)

# Lista todos os decks no banco de dados
def decks_list(request):

    all_decks = Deck.objects.order_by('name')
    context = {'decks': all_decks}
    return render(request, 'decks/decks_list.html', context)

# Homepage redireciona para a lista de decks
def home(request):
    return redirect('decks_list')

# Autocompletar nomes de cartas usando a API Scryfall
def card_autocomplete(request):
    
    query = request.GET.get('card', '')

    if len(query) > 1:
        scryfall_url = f"https://api.scryfall.com/cards/autocomplete?q={query}"
        headers = {'User-Agent': 'MagicTool/1.0'}
        try:
            response = requests.get(scryfall_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            card_names = data.get('data', [])
            return JsonResponse(card_names, safe=False)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse([], safe=False)