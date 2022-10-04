run:
	cd be_challenge_project && python manage.py runserver

test:
	cd be_challenge_project && python manage.py test

migrations:
	cd be_challenge_project && python manage.py makemigrations

migrate:
	cd be_challenge_project && python manage.py migrate