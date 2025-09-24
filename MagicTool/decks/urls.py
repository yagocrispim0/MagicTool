from django.urls import path
from . import views

urlpatterns = [
    #URL para listar decks criados
    path('', views.decks_list, name='decks_list'),
    #URL para criar um novo deck
    path('create/', views.create_deck, name = 'create_deck'),

]