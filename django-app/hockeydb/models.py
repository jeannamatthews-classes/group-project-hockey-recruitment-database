from django.db import models
from django.forms.models import model_to_dict
from hockeydb.crud_model import CRUDModel
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

class Player(CRUDModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    grad_year = models.SmallIntegerField()
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15) # As per ITU-T reccomendation E.164 (from wikipedia)
    position = models.CharField(max_length=100)
    rank = models.SmallIntegerField()  # TODO: Implement data validation on rank so that two players can't be ranked the same

    _accessible_fields = ["first_name","last_name","grad_year","date_of_birth","email","phone","position","rank"]


class Team(CRUDModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    coach_first_name = models.CharField(max_length=100)
    coach_last_name = models.CharField(max_length=100)
    coach_email = models.EmailField()
    team_website = models.URLField()

    _accessible_fields = ["name","coach_first_name","coach_last_name","coach_email"]

    @classmethod
    @CRUDModel._CRUDModel__exception_handler            # dunderscores go brrr
    @CRUDModel._CRUDModel__require_methods(["GET"])
    def api_read(cls, request : HttpRequest):
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
        
    @classmethod
    @CRUDModel._CRUDModel__exception_handler
    @CRUDModel._CRUDModel__require_methods(["GET"])
    def api_search(cls, request : HttpRequest):
        u_query : dict = request.GET.dict()

        if "all" in u_query.keys():
            query_result = cls.objects.all()

        else:
            query = {}
            for qk in u_query.keys():
                if qk in cls._accessible_fields:
                    # If a query field is in the allowed list, rename it's key to match the query format
                    query[f"{qk}__icontains"] = u_query[qk]

            if len(query) == 0:
                return JsonResponse({"status": "error", "message": cls._mesg_noquery}, status=400)

            query_result = cls.objects.filter(**query)

        objects = []
        for t in query_result:
            team = model_to_dict(t)

            players = TeamMembership.objects.filter(team_id=team["id"])
            team["players"] = []
            for player in players:
                player_data = model_to_dict(Player.objects.get(pk=player.player_id))
                player_data["number_on_team"] = player.number_on_team
                team["players"].append(player_data)

            objects.append(team)

        return JsonResponse({"status": "success", "data": objects},status=200)


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    number_on_team = models.IntegerField()


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    home_team_score = models.IntegerField()
    away_team_score = models.IntegerField()
    # W is a home win, L is a home loss, T is a tie, I is a canceled or otherwise incomplete game
    result = models.CharField(max_length=10, choices=[('W', 'Win'), ('L', 'Loss'), ('T', 'Tie'), ('I', 'Incomplete')])


class Note(CRUDModel):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
    content = models.TextField()

    _accessible_fields = ["player","content"]