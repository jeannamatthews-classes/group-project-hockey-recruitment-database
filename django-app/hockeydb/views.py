from hockeydb.models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)


def home(request):
    return JsonResponse({"message": "Welcome to the Hockey DB!"})


def get_player_by_id(request):
    if request.method == "GET" and request.GET.get("id") is not None:
        player_id = request.GET.get("id")

        try:
            player = Player.objects.get(pk=player_id)
            return JsonResponse({"status": "success", "data": model_to_dict(player)})
        except Player.DoesNotExist:
           return JsonResponse({"status": "error", "message": "Player not found."})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method or missing player ID."})
    

def get_team_by_id(request):
    if request.method == "GET" and request.GET.get("id") is not None:
        team_id = request.GET.get("id")

        try:
            team = Team.objects.get(pk=team_id)
            return JsonResponse({"status": "success", "data": model_to_dict(team)})
        except Team.DoesNotExist:
           return JsonResponse({"status": "error", "message": "Team not found."})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method or missing team ID."})


def search_player_by_name(request):
    if request.method == "GET":

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
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def search_team_by_query(request):
    if request.method == "GET":

        search_query = request.GET.get('name')  
        
        if not search_query:
            return JsonResponse({"status": "error", "message": "Missing 'name' parameter"}, status=400)
            
        teams = Team.objects.filter(name__icontains=search_query)
        

        data = [model_to_dict(team) for team in teams]
        
        if not data:
            return JsonResponse({"status": "success", "message": "No teams found", "data": []})
            
        return JsonResponse({"status": "success", "data": data})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def update_player(request, player_id):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"})
    try:
        player = Player.objects.get(id = player_id)

    except Player.DoesNotExist:
        return JsonResponse({"error": "Player not found"})
    
    fields_to_update = ['first_name', 'last_name', 'date_of_birth', 'position']

    for field in fields_to_update:
        if field in request.POST:
            setattr(player, field, request.POST[field])
    try:
        player.save()
    except Exception as e:
        return JsonResponse({"error": str(e)})
    
    return JsonResponse({
        "id": player.id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "date_of_birth": player.date_of_birth,
        "position": player.position
    })