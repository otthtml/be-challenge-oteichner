import os

import requests
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from ratelimit.decorators import ratelimit

from be_challenge_app.services import import_league, import_teams
from be_challenge_app.models import Coach, Player, Team

class ImportLeagueView(View):

    @method_decorator(ratelimit(key='ip', rate='60/h', method='POST', block=True))
    def post(self, request):
        # get league code from query string
        league_code = request.GET.get('league-code')
        if not league_code:
            return HttpResponse("No league_code provided", status=400)

        # send request to football-data.org v4 API with timeout of 5 seconds
        response = requests.get(
            f'https://api.football-data.org/v4/competitions/{league_code}',
            timeout=5,
            headers={'X-Auth-Token': os.environ.get('API_KEY')}
        )
        # check if response is successful
        if response.status_code != 200:
            return HttpResponse("League not found", status=404)

        league = import_league(response)

        # request teams from football-data.org v4 API with timeout of 5 seconds
        response = requests.get(
            f'https://api.football-data.org/v4/competitions/{league_code}/teams',
            timeout=5,
            headers={'X-Auth-Token': os.environ.get('API_KEY')}
        )
        import_teams(response, league)

        return HttpResponse("OK!")

class PlayersView(View):
    def get(self, request):
        league_code = request.GET.get('league-code')
        team_name = request.GET.get('team-name')

        if not league_code:
            return HttpResponse("No league-code provided", status=400)

        players = Player.objects.filter(team__league__code=league_code)
        if players.count() == 0:
            return HttpResponse("League not found", status=404)

        if team_name:
            players = players.filter(team__name=team_name)

        return JsonResponse(
            list(players.values(
                'name', 'position', 'date_of_birth', 'nationality', 'team__name'
            )),
            safe=False
        )

class TeamView(View):
    def get(self, request):
        team_name = request.GET.get('team-name')
        if not team_name:
            return HttpResponse("No team-name provided", status=400)

        team = Team.objects.filter(name=team_name)

        if not team.first():
            return HttpResponse("Team not found", status=404)

        if request.GET.get('with-players') == 'true':

            players = Player.objects.filter(team=team.first())
            if players.count() == 0:
                coach = Coach.objects.filter(team=team.first())
                return JsonResponse({
                    'team': team.values('name', 'tla', 'short_name', 'area', 'address').first(),
                    'players': [],
                    'coach': coach.values(
                        'name', 'date_of_birth', 'nationality'
                    ).first()
                })
            return JsonResponse({
                'team': team.values('name', 'tla', 'short_name', 'area', 'address').first(),
                'players': list(players.values(
                    'name', 'position', 'date_of_birth', 'nationality'
                )),
                'coach': ''
            })

        return JsonResponse(
            team.values('name', 'tla', 'short_name', 'area', 'address').first(),
        )

class TeamPlayersView(View):

    def get(self, request):
        team_name = request.GET.get('team-name')
        if not team_name:
            return HttpResponse("No team-name provided", status=400)

        team = Team.objects.filter(name=team_name)

        if not team.first():
            return HttpResponse("Team not found", status=404)

        players = Player.objects.filter(team=team.first())

        if players.count() == 0:
            coach = Coach.objects.filter(team=team.first())
            return JsonResponse({
                'coach': coach.values(
                    'name', 'date_of_birth', 'nationality'
                ).first()
            })

        return JsonResponse(
            list(players.values(
                'name', 'position', 'date_of_birth', 'nationality'
            )),
            safe=False
        )
