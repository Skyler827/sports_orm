from django.shortcuts import render, redirect
from django.db.models import Count
from .models import League, Team, Player
from . import team_maker


def index2(request):
    lists = [
        {
            # ...all teams in the Atlantic Soccer Conference
            "title":"Teams in the Atlantic Soccer Conference",
            "expression": League.objects.get(name="Atlantic Soccer Conference").teams.all(),
            "type": "Teams"
        }, {
            # ...all (current) players on the Boston Penguins
            "title": "Players on the Boston Penguins",
            "expression": Team.objects.get(team_name="Penguins").curr_players.all(),
            "type": "Players"
        }, {
            # ...all (current) players in the International Collegiate Baseball Conference
            "title": "Players in the ICBC",
            "expression": [
                player for team in League.objects.get(
                    name="International Collegiate Baseball Conference"
                    ).teams.all()
                for player in team.curr_players.all()
           ],
            "type":"Players"
        }, {
            # ...all (current) players in the American Conference of Amateur Football with last name "Lopez"
            "title":"Players in the ACAF with last name \"Lopez\"",
            "expression": [
                player for team in League.objects.get(
                    name="American Conference of Amateur Football"
                ).teams.all() for player in team.curr_players.filter(last_name="Lopez")],
            "type":"Players"
        }, {
            # ...all football players
            "title": "All football players",
            "expression": [
                player
                for league in League.objects.filter(name__contains="Football")
                for team in league.teams.all()
                for player in team.curr_players.all()
            ],
            "type":"Players"
        }, {
            # ...all teams with a (current) player named "Sophia"
            "title":"Teams with a player named \"Sophia\"",
            "expression":
                filter(
                    lambda team:
                        True if len(list(filter(
                            lambda player: player.first_name == "Sophia",
                            team.curr_players.all()))) > 0
                        else False,
                    Team.objects.all()),
            "type": "Teams"
        }, {
            # ...all leagues with a (current) player named "Sophia"
            "title": "Leagues with a player named \"Sophia\"",
            "type": "Leagues",
            "expression":
                filter(
                    lambda league:
                        True if len(list(
                            filter(lambda team:
                                True if len(list(
                                    filter(
                                        lambda player:
                                            player.first_name == "Sophia",
                                        team.curr_players.all()
                                    )
                                )) > 0
                                else False,
                                league.teams.all()
                            )
                        )) > 0
                        else False,
                    League.objects.all()
                )
        }, {
            # ...everyone with the last name "Flores" who DOESN'T (currently) play for the Washington Roughriders
            "title": "Players whose last name is \"Flores\" and don't play for the Roughriders",
            "expression": filter(
                lambda player:
                    player.curr_team.team_name != "Roughriders" and
                    player.curr_team.location != "Washington",
                Player.objects.filter(last_name="Flores")
            ),
            "type": "Players"
        }, {
            # ...all teams, past and present, that Samuel Evans has played with
            "title":"Teams Sam Evans has played with",
            "expression": filter(
                lambda team:
                    len(list(
                        team.all_players.filter(first_name="Samuel").filter(last_name="Evans")
                    )) > 0,
                Team.objects.all()
            ),
            "type": "Teams"
        }, {
            # ...all players, past and present, with the Manitoba Tiger-Cats
            "title": "Current and former Manitoba Tiger-Cats",
            "expression": Team.objects.get(location="Manitoba").all_players.all(),
            "type": "Players"
        }, {
            # ...all players who were formerly (but aren't currently) with the Wichita Vikings
            "title": "Former Wichita Vikings",
            "expression": filter(
                lambda player: player.curr_team.team_name != "Vikings",
                Team.objects.get(location="Wichita").all_players.all()),
            "type": "Players"
        }, {
            # ...every team that Jacob Gray played for before he joined the Oregon Colts
            "title": "Teams Jacob Gray previously played on",
            "expression": filter(
                lambda team:
                    team != Player.objects.filter(first_name="Jacob").filter(last_name="Gray").first().curr_team,
                Player.objects.filter(first_name="Jacob").filter(last_name="Gray").first().all_teams.all()),
            "type": "Teams"
        }, {
            # ...everyone named "Joshua" who has ever played in the Atlantic Federation of Amateur Baseball Players
            "title": "Joshuas who've ever played for AFABP",
            "expression": filter(
                lambda player: 0 < len(list(filter(
                    lambda team: team.league.name == "Atlantic Federation of Amateur Baseball Players",
                    player.all_teams.all()
                ))),
                Player.objects.filter(first_name="Joshua")
            ),
            "type": "Players"
        }, {
            # ...all teams that have had 12 or more players, past and present.
            "title": "Teams with over 11 players, current and former",
            "expression": filter(
                lambda team: len(list(team.all_players.all())) > 11,
                Team.objects.all()
            ),
            "type": "Teams"
        }
    ]
    # ...all players and count of teams played for, sorted by the number of teams they've played for

    last_list = [
        {
            "name": p.first_name + " "+ p.last_name,
            "teams": p.all_teams__count
        } for p in Player.objects.annotate(Count('all_teams')).order_by("-all_teams__count")
    ]
    return render(request, "leagues/index2.html", {"lists": lists, "last_list":last_list})


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
