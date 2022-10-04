run:
	if [ ! -f be_challenge_project/db.sqlite3 ]; then \
		make migrations; \
		make migrate; \
	fi
	if [ ! -d venv ]; then \
		make install; \
	fi
	
	cd be_challenge_project && python manage.py runserver

test:
	cd be_challenge_project && python manage.py test

migrations:
	cd be_challenge_project && python manage.py makemigrations

migrate:
	cd be_challenge_project && python manage.py migrate

install:
	if [ ! -d venv ]; then \
		python3 -m venv venv; \
	fi
	source venv/bin/activate && pip install -r requirements.txt

shell:
	cd be_challenge_project && python manage.py shell