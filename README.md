# Hockey-Recruiting-Database

description TODO

# Docker
The building and running process is handled by docker with a makefile. By default, docker will build the development stack from scratch whenever you run `make`.
## Development Mode Commands
- `make` or `make build-dev`:
Build and run the development environment. This just builds the django image and exposes it at port 8000 on your computer. Django will use the SQLite backend, and some default (insecure) settings to make development easier.
- `make run-dev`:
Same as above, but may not rebuild the image. Good for if building takes a while on your computer and you haven't made any changes.
## Production Mode Commands
- `make build-prod`:
Build and run the production environment. This currently builds the django and an nginx image, and exposes them at port 80 on your computer. Nginx will serve `/static` and `/media` like a produciton environment. This disables django's debugging features, and generaly shouldn't be used unless you're deploying testing production-only features. The production environment is not fully complete, and currently lacks a MySQL server instance, instead relying on the SQLite backend. Pay careful attention to the docker logs, as a proper production setup requires environment variables to be set in docker-compose.prod.yaml.
- `make run-prod`:
Same as above, but may not rebuild the image. Good for if building takes a while on your computer and you haven't made any changes.
## Utilities
- `make clean`:
Deletes all built container images. It is necessary to run this when you're switching between development and production environments, otherwise you will get an error from docker. 