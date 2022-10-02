import os

import requests
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View

class ImportLeagueView(View):
    def get(self, request):
        # get league code from query string
        league_code = request.GET.get('league-code')
        if not league_code:
            return HttpResponse("No league_code provided", status=400)

        # send request to football-data.org v4 API with timeout of 5 seconds
        response = requests.get(
            f'https://api.football-data.org/v4/competitions/{league_code}/teams', 
            timeout=5,
            headers={'X-Auth-Token': os.environ.get('API_KEY')}
        )

        return HttpResponse("OK!")
