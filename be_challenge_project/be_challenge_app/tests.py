from django.test import TestCase

# Create your tests here.

class TestImportLeagueView(TestCase):
    def test_get_returns_400_if_no_league_code(self):
        response = self.client.get("/api/import-league/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"No league_code provided")