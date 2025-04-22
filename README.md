# Hockey-Recruiting-Database

A project that allows tracking of Hockey recruits. Built with a django backend and a vue.js frontend.

# Docker
The building and running process is handled by docker with a makefile. By default, docker will build the development stack from scratch whenever you run `make`.
## Development Mode Commands
- `make` or `make dev`:
Build and run the development environment. This builds the Django backend, and the vue frontend, and exposes them both at port 80 on your device. Django will use the SQLite backend, and some default (insecure) settings to make development easier.
## Production Mode Commands
- `make prod`:
Build and run the production environment. This currently builds the django and an nginx image, and exposes them at port 80 on your computer. Nginx will serve `/static` like a production environment. This disables django's debugging features, and generally shouldn't be used unless you're deploying testing production-only features. Pay careful attention to the docker logs, as a proper production setup requires environment variables to be set in docker-compose.prod.yaml.
## Cleanup
- `make clean`:
Delete all saved data and containers. This is highly destructive and irreversible.
- `make clean-containers`:
Delete all saved containers.
- `make clean-data`:
Delete saved data volumes. This is destructive and irreversible.
## Shells
- `make sh-django`:
Opens a shell into the django container. The container must already be running for this to work.
- `make sh-mysql`:
Opens a shell into the mysql container. The container must already be running for this to work.
- `make sh-nginx`:
Opens a shell into the nginx container. The container must already be running for this to work.
## Miscellaneous Utilities
- `make su-django`:
Create a django superuser. Effectively runs `python3 manage.py createsuperuser` inside the django container. The container must already be running for this to work. Because django users are stored in the database, this does not carry across development/ production environments or database wipes.