from hockeydb.models import *
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging
import json

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


@require_http_methods(["POST"])
def change_player_number_on_team(request):
    body = json.loads(request.body)
    try:
        membership = TeamMembership.objects.get(
            player_id=body["player_id"],
            team_id=body["team_id"]
        )
    except TeamMembership.DoesNotExist:
        return JsonResponse({"status":"error","message":"Player not on team"},status=400)
    
    try:
        membership.number_on_team = body["number_on_team"]
        membership.save()
    except Exception as e :
        return JsonResponse({"status":"error","message":f"Missing or invalid field, {e}"},status=400)
    return JsonResponse({"status":"success","data":model_to_dict(membership)},status=200)



@require_http_methods(["POST"])
def add_player_to_team(request):
    body = json.loads(request.body)

    membership = TeamMembership()

    for field in ["player_id","team_id","number_on_team"]:
        try:
            setattr(membership,field,body[field])
        except KeyError:
            pass # Ignore fields that don't exist

    try:
        membership.save()
    except Exception as e :
        return JsonResponse({"status":"error","message":f"Missing or invalid field, {e}"},status=400)

    return JsonResponse({"status":"success","data":model_to_dict(membership)},status=200)


@require_http_methods(["POST"])
def remove_player_from_team(request):
    body = json.loads(request.body)

    TeamMembership.objects.delete(
        player_id=body["player_id"],
        team_id=body["team_id"]
    )
    return JsonResponse({"status":"success"},status=200)
