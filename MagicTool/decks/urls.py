from django.urls import path
from . import views

urlpatterns = [

    #URL para ver detalhes de um deck específico
    path('<int:deck_id>/', views.deck_detail, name='deck_detail'),
    #URL para listar decks criados
    path('', views.decks_list, name='decks_list'),
    #URL para criar um novo deck
    path('create/', views.create_deck, name = 'create_deck'),
    #
    path('api/card-autocomplete/', views.card_autocomplete, name='card_autocomplete'),

]