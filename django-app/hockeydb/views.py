from hockeydb.models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
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
    

def get_team(request):
    pass

def get_note(request):
    pass

@require_http_methods(["GET"])
def search_player(request):
    allow_query = ["first_name","last_name"]
    u_query : dict = request.GET.dict()

    query = {}
    for qk in u_query.keys():
        if qk in allow_query:
            # If a query field is in the allowed list, rename it's key to match the query format
            query[f"{qk}__icontains"] = u_query[qk]

    if len(query) == 0:
        return JsonResponse({"status": "error", "message": "Missing valid query parameters"}, status=400)

    query_result = Player.objects.filter(**query)

    players = [model_to_dict(p) for p in query_result]

    return JsonResponse({"status": "success", "data": players},status=200)

def search_team(request):
    pass

def search_note(request):
    pass

@csrf_exempt
@require_http_methods(["POST"])
def update_player(request):
    allow_update = ["first_name","last_name","date_of_birth","position"]
    body = json.loads(request.body)

    try:
        player_id = body["id"]
    except KeyError:
        return JsonResponse({"status":"error","message":"Missing 'id' parameter"},status=400)
    
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({"status":"error","message":f"No player with id {player_id}"},status=404)

    for field in allow_update:
        try:
            setattr(player,field,body[field])
        except KeyError:
            pass # Ignore fields that don't exist

    try:
        player.save()
    except Exception as e:
        return JsonResponse({"status":"error","message":str(e)},status=400)
    
    return JsonResponse({"status":"success","data":model_to_dict(player)},status=200)

def update_team(request):
    pass

def update_note():
    pass

@csrf_exempt
@require_http_methods("POST")
def create_player(request):
    allow_create = ["first_name","last_name","date_of_birth","position"]
    body = json.loads(request.body)

    player = Player()

    for field in allow_create:
        try:
            setattr(player,field,body[field])
        except KeyError:
            pass # Ignore fields that don't exist

    try:
        player.save()
    except Exception as e:
        return JsonResponse({"status":"error","message":str(e)},status=400)

    return JsonResponse({"status":"success","data":model_to_dict(player)},status=200)

def create_team():
    pass

def create_note():
    pass

def update_player_teams():
    pass

def add_player_to_team():
    pass
