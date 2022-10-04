import os

import requests
from django.http import Http404, HttpResponse
from django.views import View

from .models import League

class ImportLeagueView(View):
    def get(self, request):
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
        
        import_league(response)
        # import_team(response)

        return HttpResponse("OK!")

def import_league(response):
    # get league name from response
    league_name = response.json().get('name')
    # get league code from response
    league_code = response.json().get('code')
    # get area name from response
    area_name = response.json().get('area').get('name')

    # create league object
    league = League.objects.create(
        name=league_name,
        code=league_code,
        area=area_name
    )