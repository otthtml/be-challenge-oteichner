from django.urls import path

from .views import ImportLeagueView

urlpatterns = [
    # path that takes a query string with a league code
    path("import-league/", ImportLeagueView.as_view()),
]