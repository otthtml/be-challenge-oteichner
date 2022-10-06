from django.test import TestCase

from be_challenge_app.models import League, Team, Player

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
            "id": 1,
            "name": "Mocked Player",
            "position": "Mocked Position",
            "date_of_birth": "2000-01-01",
            "nationality": "Mocked Country",
        },
        {
            "id": 2,
            "name": "Mocked Player2",
            "position": "Mocked Position2",
            "date_of_birth": "2000-01-02",
            "nationality": "Mocked Country2",
        }
    ]

    def _create_mocked_objects(self):
        league = League.objects.create(
            name="Mocked League",
            area="Mocked Area",
            code="PL"
        )
        team = Team.objects.create(
            name="Mocked Team",
            short_name="MT",
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
            short_name="MT2",
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

    def test_get_returns_400_if_no_league_code(self):
        response = self.client.get("/api/players/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"No league-code provided")

    def test_get_returns_404_if_league_not_found(self):
        response = self.client.get("/api/players/?league-code=not-found")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"League not found")

    def test_get_returns_players(self):
        self._create_mocked_objects()
        response = self.client.get("/api/players/?league-code=PL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.mocked_players)

    def test_get_returns_players_from_team(self):
        self._create_mocked_objects()
        response = self.client.get("/api/players/?league-code=PL&team-name=Mocked Team")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.mocked_players[0]])
