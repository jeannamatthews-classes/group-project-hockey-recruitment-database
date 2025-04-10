from django.db import models


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    position = models.CharField(max_length=100)

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    coach_first_name = models.CharField(max_length=100)
    coach_last_name = models.CharField(max_length=100)
    coach_email = models.CharField(max_length=100)


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

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE
    )
    content = models.TextField()