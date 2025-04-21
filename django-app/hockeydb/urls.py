"""
URL configuration for hockeydb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django-app.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from hockeydb import views

urlpatterns = [
    path('api/', views.home, name='home'), #homepage
    
    path('api/get/player', views.get_player, name='get_player'), #returns a json object representing a player
    path('api/get/team', views.get_team, name='get_team'), #returns a json object representing a team
    path('api/get/note', views.get_note, name='get_note'),
    
    path('api/search/player', views.search_player, name='players_list'), #returns a list of players matching first name and last name query
    path('api/search/team', views.search_team, name ='teams_list'),
    path('api/search/note', views.search_note, name ='notes_list'),
    
    path('api/update/player', views.update_player, name='update_player'),
    path('api/update/team', views.update_team, name='update_team'),
    path('api/update/team_membership', views.change_player_number_on_team, name='change_player_number_on_team'),
    path('api/update/note', views.update_note, name='update_note'),
    
    path('api/create/player', views.create_player, name='create_player'),
    path('api/create/team', views.create_team, name='create_team'),
    path('api/create/team_membership', views.add_player_to_team, name='add_player_to_team'),
    path('api/create/note', views.create_note, name='create_note'),
    
    path('api/delete/player', views.delete_player, name='delete_player'),
    path('api/delete/team', views.delete_team, name='delete_team'),
    path('api/delete/team_membership', views.remove_player_from_team, name='remove_player_from_team'),
    path('api/delete/note', views.delete_note, name='delete_note')
]
