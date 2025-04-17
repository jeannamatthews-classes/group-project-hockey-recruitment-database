from hockeydb.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def home(request):
    return JsonResponse({"message": "Welcome to the Hockey DB!"})

def get_player(request):
    return Player.api_read(request)

def get_team(request):
    return Team.api_read(request)

def get_note(request):
    return Note.api_read(request)

def search_player(request):
    return Player.api_search(request)

def search_team(request):
    return Team.api_search(request)

def search_note(request):
    return Note.api_search(request)

@csrf_exempt
def update_player(request):
    return Player.api_update(request)

@csrf_exempt
def update_team(request):
    return Team.api_update(request)

@csrf_exempt
def update_note(request):
    return Note.api_update(request)

@csrf_exempt
def create_player(request):
    return Player.api_create(request)

@csrf_exempt
def create_team(request):
    return Team.api_create(request)

@csrf_exempt
def create_note(request):
    return Note.api_create(request)

@csrf_exempt
def delete_player(request):
    return Player.api_delete(request)

@csrf_exempt
def delete_team(request):
    return Team.api_delete(request)

@csrf_exempt
def delete_note(request):
    return Note.api_delete(request)

def update_player_teams():
    pass

def add_player_to_team():
    pass
