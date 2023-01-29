Leo Getz is the Discord bot server.

Setup instructions:

* clone repo, `cd` into `requests-scanner/`, and checkout "feature/django" branch

  `git checkout feature/django`

* copy env.sample to .env and get the following values from a buddy:
    * DJANGO_SECRET_KEY
    * PGCRYPTO_SECRET_KEY
    * DISCORD_TOKEN
    * PLEX_USERNAME
    * PLEX_PASSWORD

* open terminal and `cd` to `/packages/leo-getz`

* create docker volume

  `docker volume create --name=leo_getz_postgres`

* build bot container

  `docker-compose build bot`

* migrate dev database

  `./bin/dcp-django-admin migrate`

* load initial admin user into database

  `./bin/dcp-django-admin loaddata initial_dev_data.json`

* run all unit tests vis shell script

  `./bin/dcp-run-tests`

* run the web server

  `docker-compose up bot`

  you can now access the admin page at `0.0.0.0/8053` and login with `admin` and `password`

* start the Discord bot `$ ./bin/dcp-django-admin start_discord_bot`