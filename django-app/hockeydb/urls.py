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
from django.contrib import admin
from django.urls import path
from hockeydb import views

urlpatterns = [
    path('', views.home, name='home'), #homepage
    path('admin/', admin.site.urls),

    path('api/player/get', views.get_player_by_id, name='get_player'), #returns a json object representing a player
    path('api/player/search', views.search_player_by_name, name='players_list'), #returns a list of players matching first name and last name query
    path('api/player/update', views.update_player, name='update_player'),
    path('api/player/create', views.create_player, name='create_player'),

    path('api/team/get', views.get_team_by_id, name='get_team'), #returns a json object representing a team
    path('api/team/search', views.search_team_by_name, name ='teams_list'),
    path('api/team/update', views.update_team, name='update_team'),
    path('api/team/create', views.create_team, name='create_team'),

    path('api/note/get', views.get_note_by_id, name='get_note'),
    path('api/note/search', views.search_note_by_query, name ='notes_list'),
    path('api/note/update', views.update_note, name='update_note'),
    path('api/note/create', views.create_note, name='create_note'),

    path('api/player_teams/get', views.get_player_teams, name='get_player_teams'),
    path('api/player_teams/update', views.update_player_teams, name='get_player_teams'),
    path('api/player_teams/add', views.add_player_to_team, name='get_player_teams'),

]
