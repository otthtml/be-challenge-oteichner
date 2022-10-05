from be_challenge_app.models import League, Team, Player, Coach


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

    return league

def import_teams(response, related_league):
    # for each team in response, create team object
    for team in response.json().get('teams'):
        # get team name from response
        team_name = team.get('name')
        # get team short name from response
        team_short_name = team.get('shortName')
        # get team area name from response
        team_area_name = team.get('area').get('name')
        # get team address from response
        team_address = team.get('address')

        # if team already exists, add team to league
        if Team.objects.filter(name=team_name).exists(): # pylint: disable=no-member
            team = Team.objects.get(name=team_name) # pylint: disable=no-member
            team.league.add(related_league)
            continue

        # else create team object
        db_team = Team.objects.create(
            name=team_name,
            short_name=team_short_name,
            area=team_area_name,
            address=team_address
        )
        db_team.league.add(related_league)

        # if team has players, create player objects
        if team.get('squad'):
            import_players(team.get('squad'), db_team)
        else:
            # else create coach object
            import_coach(team.get('coach'), db_team)

def import_players(players, related_team):
    for player in players:
        # get player name from response
        player_name = player.get('name')
        # get player position from response
        player_position = player.get('position')
        # get player date of birth from response
        player_date_of_birth = player.get('dateOfBirth')
        # get player country of birth from response
        player_country_of_birth = player.get('nationality')

        # create player object
        db_player = Player.objects.create(
            name=player_name,
            position=player_position,
            date_of_birth=player_date_of_birth,
            nationality=player_country_of_birth
        )
        db_player.save()
        db_player.team.add(related_team)

def import_coach(coach, related_team):
    # get coach name from response
    coach_name = coach.get('name')
    # get coach date of birth from response
    coach_date_of_birth = coach.get('dateOfBirth')
    # get coach country of birth from response
    coach_country_of_birth = coach.get('nationality')

    # create coach object
    db_coach = Coach.objects.create(
        name=coach_name,
        date_of_birth=coach_date_of_birth,
        nationality=coach_country_of_birth
    )
    db_coach.save()
    db_coach.team.add(related_team)
