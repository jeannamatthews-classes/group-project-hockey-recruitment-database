from hockeydb.models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict


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
