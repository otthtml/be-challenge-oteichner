from django.urls import path

from be_challenge_app.views import ImportLeagueView, PlayersView

urlpatterns = [
    # path that takes a query string with a league code
    path("import-league/", ImportLeagueView.as_view()),
    path("players/", PlayersView.as_view()),
]
