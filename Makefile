VENV := . env/bin/activate
PPATH := $(VENV) && cd be_challenge_project

run:
	if [ ! -f be_challenge_project/db.sqlite3 ]; then \
		make migrations; \
		make migrate; \
	fi
	if [ ! -d env ]; then \
		make install; \
	fi
	
	$(PPATH) && python manage.py runserver

test:
	$(PPATH) && python manage.py test

migrations:
	$(PPATH) && python manage.py makemigrations

migrate:
	$(PPATH) && python manage.py migrate

install:
	if [ ! -d env ]; then \
		python3 -m venv env; \
	fi
	$(VENV) && pip install -r requirements.txt

shell:
	$(PPATH) && python manage.py shell