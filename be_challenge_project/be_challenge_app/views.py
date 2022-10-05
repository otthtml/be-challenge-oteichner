import os

import requests
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from ratelimit.decorators import ratelimit

from be_challenge_app.services import import_league, import_teams

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
