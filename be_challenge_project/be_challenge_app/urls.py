from django.urls import path

from be_challenge_app.views import ImportLeagueView, PlayersView, TeamView

urlpatterns = [
    path("import-league/", ImportLeagueView.as_view()),
    path("players/", PlayersView.as_view()),
    path("team/", TeamView.as_view()),
]
