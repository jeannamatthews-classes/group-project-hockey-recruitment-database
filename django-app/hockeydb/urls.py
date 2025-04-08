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
    path('api/get/player', views.get_player_by_id, name='get_player'), #returns a json object representing a player
    path('api/get/team', views.get_team_by_id, name='get_team'), #returns a json object representing a team
    path('api/search/team', views.search_team_by_query, name ='teams_list'),
    path('api/search/player', views.search_player_by_name, name='players_list'), #returns a list of players matching first name and last name query
    #path('players/<int:player_id>/update', views.update_player, name='update_player')
]
