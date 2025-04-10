from hockeydb.models import *
from django.http import HttpRequest, JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import models
import json
import logging
import json

logger = logging.getLogger(__name__)

def home(request):
    return JsonResponse({"message": "Welcome to the Hockey DB!"})

@require_http_methods(["GET"])
def get_player(request):
    if request.GET.get("id") is not None:
        player_id = request.GET.get("id")

        try:
            player = Player.objects.get(pk=player_id)
            return JsonResponse({"status": "success", "data": model_to_dict(player)},status=200)
        except Player.DoesNotExist:
           return JsonResponse({"status": "error", "message": "Player not found."},status=404)
    else:
        return JsonResponse({"status": "error", "message": "Missing player ID."},status=400)

@require_http_methods(["GET"])
def get_team(request):
    if request.GET.get("id") is None:
        return JsonResponse({"status": "error", "message": "Missing team ID."},status=400)
 
    team_id = request.GET.get("id")
 
    try:
        team = model_to_dict(Team.objects.get(pk=team_id))

        # Get the players in the team
        players = TeamMembership.objects.filter(team_id=team_id)
        team["players"] = []
        for player in players:
            player_data = model_to_dict(Player.objects.get(pk=player.player_id))
            player_data["number_on_team"] = player.number_on_team
            team["players"].append(player_data)
 
        return JsonResponse({"status": "success", "data": team},status=200)
    except Team.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Team not found."},status=404)

@require_http_methods(["GET"])
def get_note(request):
    if request.GET.get("id") is not None:
        note_id = request.GET.get("id")

        try:
            note = Note.objects.get(pk=note_id)
            return JsonResponse({"status": "success", "data": model_to_dict(note)},status=200)
        except Note.DoesNotExist:
           return JsonResponse({"status": "error", "message": "Note not found."},status=404)
    else:
        return JsonResponse({"status": "error", "message": "Missing note ID."},status=400)

@require_http_methods(["GET"])
def __search_by_query(request : HttpRequest, allow_query : list[str], model : models.Model):
    u_query : dict = request.GET.dict()

    query = {}
    for qk in u_query.keys():
        if qk in allow_query:
            # If a query field is in the allowed list, rename it's key to match the query format
            query[f"{qk}__icontains"] = u_query[qk]

    if len(query) == 0:
        return JsonResponse({"status": "error", "message": "Missing valid query parameters"}, status=400)

    query_result = model.objects.filter(**query)

    objects = [model_to_dict(p) for p in query_result]

    return JsonResponse({"status": "success", "data": objects},status=200)

def search_player(request):
    return __search_by_query(request,["first_name","last_name","date_of_birth","position",],Player)

def search_team(request):
    return __search_by_query(request,["name","coach_first_name","coach_last_name","coach_email"],Team)

def search_note(request):
    return __search_by_query(request,["player","content"],Note)

@require_http_methods(["POST"])
def __update_by_id(request : HttpRequest, allow_update : list[str], model : models.Model):
    body = json.loads(request.body)

    try:
        id = body["id"]
    except KeyError:
        return JsonResponse({"status":"error","message":"Missing 'id' parameter"},status=400)
    
    try:
        obj = model.objects.get(id=id)
    except model.DoesNotExist:
        return JsonResponse({"status":"error","message":f"No player with id {id}"},status=404)

    for field in allow_update:
        try:
            setattr(obj,field,body[field])
        except KeyError:
            pass # Ignore fields that don't exist

    try:
        obj.save()
    except Exception as e:
        return JsonResponse({"status":"error","message":str(e)},status=400)
    
    return JsonResponse({"status":"success","data":model_to_dict(obj)},status=200)

@csrf_exempt
def update_player(request):
    return __update_by_id(request,["first_name","last_name","date_of_birth","position"],Player)

@csrf_exempt
def update_team(request):
    return __update_by_id(request,["name","coach_first_name","coach_last_name","coach_email"],Team)

@csrf_exempt
def update_note(request):
    return __update_by_id(request,["player","content"],Note)

@require_http_methods("POST")
def __create(request : HttpRequest, allow_create : list["str"], model : models.Model):
    body = json.loads(request.body)

    obj = model()

    for field in allow_create:
        try:
            setattr(obj,field,body[field])
        except KeyError:
            pass # Ignore fields that don't exist

    try:
        obj.save()
    except Exception as e:
        return JsonResponse({"status":"error","message":str(e)},status=400)

    return JsonResponse({"status":"success","data":model_to_dict(obj)},status=200)

@csrf_exempt
def create_player(request):
    return __create(request,["first_name","last_name","date_of_birth","position"],Player)

@csrf_exempt
def create_team(request):
    return __create(request,["name","coach_first_name","coach_last_name","coach_email"],Team)

@csrf_exempt
def create_note(request):
    return __create(request,["player","content"],Note)

def update_player_teams():
    pass

def add_player_to_team():
    pass
