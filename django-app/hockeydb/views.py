from hockeydb.models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods
import logging
import json

logger = logging.getLogger(__name__)


def home(request):
    return JsonResponse({"message": "Welcome to the Hockey DB!"})


@require_http_methods(["GET"])
def get_player_by_id(request):
    if request.GET.get("id") is None:
        return JsonResponse({"status": "error", "message": "Invalid request: missing player ID."})

    player_id = request.GET.get("id")

    try:
        player = Player.objects.get(pk=player_id)
        return JsonResponse({"status": "success", "data": model_to_dict(player)})
    except Player.DoesNotExist:
       return JsonResponse({"status": "error", "message": "Player not found."})


@require_http_methods(["GET"])
def get_team_by_id(request):
    if request.GET.get("id") is None:
        return JsonResponse({"status": "error", "message": "Invalid request: missing team ID."})

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

        return JsonResponse({"status": "success", "data": team})
    except Team.DoesNotExist:
       return JsonResponse({"status": "error", "message": "Team not found."})


@require_http_methods(["GET"])
def get_player_teams(request):
    if request.GET.get("id") is None:
        return JsonResponse({"status": "error", "message": "Invalid request: missing player ID."})

    player_id = request.GET.get("id")

    try:
        teams = TeamMembership.objects.filter(player_id=player_id).values("team_id", "number_on_team")
        return JsonResponse({"status": "success", "data": list(teams)})
    except Player.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Player not found."})


def get_note_by_id(request):
    pass


@require_http_methods(["GET"])
def search_player_by_name(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')

    if not first_name and not last_name:
        return JsonResponse({"status": "error", "message": "Missing 'first_name' or 'last_name' parameter"}, status=400)

    query = {}
    if first_name:
        query["first_name__icontains"] = first_name
    if last_name:
        query["last_name__icontains"] = last_name

    players = Player.objects.filter(**query)

    # Serialize all matching players
    data = [model_to_dict(player) for player in players]

    if not data:
        return JsonResponse({"status": "success", "data": []})

    return JsonResponse({"status": "success", "data": data})


@require_http_methods(["GET"])
def search_team_by_name(request):
    search_query = request.GET.get('name')

    if not search_query:
        return JsonResponse({"status": "error", "message": "Missing 'name' parameter"}, status=400)

    teams = Team.objects.filter(name__icontains=search_query)


    data = [model_to_dict(team) for team in teams]

    if not data:
        return JsonResponse({"status": "success", "message": "No teams found", "data": []})

    return JsonResponse({"status": "success", "data": data})


@require_http_methods(["GET"])
def search_note_by_query(request):
    search_query = request.GET.get('query')

    if not search_query:
        return JsonResponse({"status": "error", "message": "Missing 'query' parameter"}, status=400)

    notes = Note.objects.filter(content__icontains=search_query)


    data = [model_to_dict(note) for note in notes]

    if not data:
        return JsonResponse({"status": "success", "message": "No notes found", "data": []})

    return JsonResponse({"status": "success", "data": data})


@require_http_methods(["POST"])
def update_player(request):
    body = json.loads(request.body)

    try:
        player_id = body["id"]
    except KeyError:
        return JsonResponse({"status":"error","message":"Missing 'id' parameter"},status=400)
    try:
        player = Player.objects.get(id=player_id)
    except Player.DoesNotExist:
        return JsonResponse({"status":"error","message":f"No player with id {player_id}"},status=400)


    for field in ["first_name","last_name","date_of_birth","position"]:
        try:
            setattr(player,field,body[field])
        except KeyError:
            pass # Ignore fields that don't exist

    return JsonResponse({"status":"success","player":dict(player)},status=200)

def update_team(request):
    pass

def update_note():
    pass

@require_http_methods(["POSST"])
def create_player(request):
    body = json.loads(request.body)

    player = Player()

    for field in ["first_name","last_name","date_of_birth","position"]:
        try:
            setattr(player,field,body[field])
        except KeyError:
            pass # Ignore fields that don't exist

    try:
        player.save()
    except Exception as e :
        return JsonResponse({"status":"error","message":f"Missing or invalid field, {e}"},status=400)

    return JsonResponse({"status":"success","player":dict(player)},status=200)

def create_team():
    pass

def create_note():
    pass