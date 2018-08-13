from django.shortcuts import render, redirect
from .models import League, Team, Player
from . import team_maker


def index(request):
    context = {
        # ...all baseball leagues
        "all_leagues": League.objects.all(),
        # ...all womens' leagues
        "all_womens_leagues": League.objects.filter(name__contains="Women"),
        # ...all leagues where sport is any type of hockey
        "any_hockey": League.objects.filter(name__contains="Hockey"),
        # ...all leagues where sport is something OTHER THAN football
        "non_footaball":
            League.objects.exclude(name__contains="Football"),
        # ...all leagues that call themselves "conferences"
        "conference_leagues": League.objects.filter(name__contains="Conf"),
        # ...all leagues in the Atlantic region
        "atlantic_leagues": League.objects.filter(name__icontains="Atlantic"),
        # ...all teams based in Dallas
        "dallas_teams": Team.objects.filter(location="Dallas"),
        # ...all teams named the Raptors
        "raptors_teams": Team.objects.filter(team_name="Raptors"),
        # ...all teams whose location includes "City"
        "teams_in_city_cities": Team.objects.filter(location__contains="City"),
        # ...all teams whose names begin with "T"
        "teams_startwith_t": Team.objects.filter(team_name__startswith="T"),
        # ...all teams, ordered alphabetically by location
        "alphabetically_by_location": Team.objects.order_by("location"),
        # ...all teams, ordered by team name in reverse alphabetical order
        "reverse_alpha_by_team_name": Team.objects.order_by("-team_name"),
        # ...every player with last name "Cooper"
        "last_name_cooper": Player.objects.filter(last_name="Cooper"),
        # ...every player with first name "Joshua"
        "first_name_joshua": Player.objects.filter(first_name="Joshua"),
        # ...every player with last name "Cooper"
        # EXCEPT those with "Joshua" as the first name
        "conditional_select": Player.objects \
            .filter(last_name__contains="Cooper") \
            .exclude(first_name__contains="Joshua"),

        # ...all players with first name "Alexander" OR first name "Wyatt"
        "players_alex_or_wyatt": Player.objects.filter(
            first_name__in=["Alexander", "Wyatt"])
    }
    return render(request, "leagues/index.html", context)


def make_data(request):
    team_maker.gen_leagues(10)
    team_maker.gen_teams(50)
    team_maker.gen_players(200)

    return redirect("index")
