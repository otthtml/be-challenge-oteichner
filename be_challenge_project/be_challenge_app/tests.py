from copy import deepcopy
from django.test import TestCase

from be_challenge_app.models import Coach, League, Team, Player

mocked_team = {
    'team': {
        "name": "Mocked Team",
        "tla": "MT",
        "short_name": "Team",
        "area": "Mocked Area",
        "address": "Mocked Address",
    },
    'players': [],
    'coach': '',
}

mocked_team_with_players = mocked_team.copy()
mocked_team_with_players['players'] = [
    {
        "name": "Mocked Player",
        "position": "Mocked Position",
        "date_of_birth": "2000-01-01",
        "nationality": "Mocked Country",
    }
]

mocked_team_with_coach = deepcopy(mocked_team)
mocked_team_with_coach['coach'] = {
    "name": "Mocked Coach",
    "date_of_birth": "2000-01-01",
    "nationality": "Mocked Country",
}
mocked_team_with_coach["team"]["name"] = "Mocked Team with coach"
mocked_team_with_coach["team"]["tla"] = "MTC"
mocked_team_with_coach["team"]["short_name"] = "Team with coach"

class TestImportLeagueView(TestCase):
    def test_post_returns_400_if_no_league_code(self):
        response = self.client.post("/api/import-league/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"No league_code provided")

    def test_post_returns_404_if_league_not_found(self):
        response = self.client.post("/api/import-league/?league-code=not-found")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"League not found")

    def test_post_creates_league_team_player(self):
        self.assertEqual(League.objects.count(), 0)
        self.assertEqual(Team.objects.count(), 0)
        self.assertEqual(Player.objects.count(), 0)
        response = self.client.post("/api/import-league/?league-code=PL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK!")
        self.assertGreater(League.objects.count(), 0)
        self.assertGreater(Team.objects.count(), 0)
        self.assertGreater(Player.objects.count(), 0)

class PlayersView(TestCase):
    mocked_players = [
        {
            "name": "Mocked Player",
            "position": "Mocked Position",
            "date_of_birth": "2000-01-01",
            "nationality": "Mocked Country",
            "team__name": "Mocked Team",
        },
        {
            "name": "Mocked Player2",
            "position": "Mocked Position2",
            "date_of_birth": "2000-01-02",
            "nationality": "Mocked Country2",
            "team__name": "Mocked Team2",
        }
    ]

    def test_get_returns_400_if_no_league_code(self):
        response = self.client.get("/api/players/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"No league-code provided")

    def test_get_returns_404_if_league_not_found(self):
        response = self.client.get("/api/players/?league-code=not-found")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"League not found")

    def test_get_returns_players(self):
        _create_mocked_objects()
        response = self.client.get("/api/players/?league-code=PL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.mocked_players)

    def test_get_returns_players_from_team(self):
        _create_mocked_objects()
        response = self.client.get("/api/players/?league-code=PL&team-name=Mocked Team")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.mocked_players[0]])


class TeamView(TestCase):

    def test_get_returns_400_if_no_team_name(self):
        response = self.client.get("/api/team/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"No team-name provided")

    def test_get_returns_404_if_team_not_found(self):
        response = self.client.get("/api/team/?team-name=not-found")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Team not found")

    def test_get_returns_team(self):
        _create_mocked_objects()
        response = self.client.get("/api/team/?team-name=Mocked Team")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mocked_team["team"])

    def test_get_returns_team_with_players(self):
        _create_mocked_objects()
        response = self.client.get("/api/team/?team-name=Mocked Team&with-players=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mocked_team_with_players)

    def test_get_returns_team_with_coach(self):
        _create_mocked_objects()
        response = self.client.get("/api/team/?team-name=Mocked Team with coach&with-players=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mocked_team_with_coach)


class TestTeamPlayersView(TestCase):
    def test_get_returns_400_if_no_team_name(self):
        response = self.client.get("/api/team-players/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"No team-name provided")

    def test_get_returns_404_if_team_not_found(self):
        response = self.client.get("/api/team-players/?team-name=not-found")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Team not found")

    def test_get_returns_players(self):
        _create_mocked_objects()
        response = self.client.get("/api/team-players/?team-name=Mocked Team")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mocked_team_with_players['players'])

    def test_get_returns_coach(self):
        _create_mocked_objects()
        response = self.client.get("/api/team-players/?team-name=Mocked Team with coach")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["coach"], mocked_team_with_coach["coach"])

def _create_mocked_objects():
    league = League.objects.create(
        name="Mocked League",
        area="Mocked Area",
        code="PL"
    )
    team = Team.objects.create(
        name="Mocked Team",
        tla="MT",
        short_name="Team",
        area="Mocked Area",
        address="Mocked Address",
    )
    team.league.add(league)
    player = Player.objects.create(
        name="Mocked Player",
        position="Mocked Position",
        date_of_birth="2000-01-01",
        nationality="Mocked Country",
    )
    player.team.add(team)

    team2 = Team.objects.create(
        name="Mocked Team2",
        tla="MT2",
        short_name="Team2",
        area="Mocked Area2",
        address="Mocked Address2",
    )
    team2.league.add(league)
    player2 = Player.objects.create(
        name="Mocked Player2",
        position="Mocked Position2",
        date_of_birth="2000-01-02",
        nationality="Mocked Country2",
    )
    player2.team.add(team2)

    team_with_coach = Team.objects.create(
        name="Mocked Team with coach",
        tla="MTC",
        short_name="Team with coach",
        area="Mocked Area",
        address="Mocked Address",
    )
    team_with_coach.league.add(league)
    coach = Coach.objects.create(
        name="Mocked Coach",
        date_of_birth="2000-01-01",
        nationality="Mocked Country",
    )
    coach.team.add(team_with_coach)
