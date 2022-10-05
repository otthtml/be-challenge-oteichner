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
        response = self.client.post("/api/import-league/?league-code=PL")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK!")
        self.assertGreater(League.objects.count(), 0)
        self.assertGreater(Team.objects.count(), 0)
        self.assertGreater(Player.objects.count(), 0)
