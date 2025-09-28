from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    #URL para editar os detalhes de um deck específico
    path('<int:deck_id>/edit/', views.edit_deck, name='edit_deck'),
    #URL para ver detalhes de um deck específico
    path('<int:deck_id>/', views.deck_detail, name='deck_detail'),
    #URL para listar decks criados
    path('deck_list', views.decks_list, name='decks_list'),
    #URL para criar um novo deck
    path('create/', views.create_deck, name = 'create_deck'),
    #
    path('api/card-autocomplete/', views.card_autocomplete, name='card_autocomplete'),

]