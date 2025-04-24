# (Re-)build and run the current stack
dev:
	echo "Building and running development stack"
	mkdir -p data
	touch data/db.sqlite3
	docker compose -f docker-compose.dev.yaml up --build

# (Re-)build and run a production-ready stack
prod:
	echo "Building and running production stack"
	docker compose -f docker-compose.prod.yaml up --build --detach

# Clean everything (this is highly destructive!)
clean: clean-containers clean-data

# Remove existing containers
clean-containers:
	docker compose -f docker-compose.dev.yaml rm
	docker compose -f docker-compose.prod.yaml rm

# Delete the data directory
clean-data:
	rm -rI ./data

# Shell into django
sh-django:
	docker exec -it hockeydb-django sh

# Shell into mysql
sh-mysql:
	docker exec -it hockeydb-mysql sh

# Shell into nginx
sh-nginx:
	docker exec -it hockeydb-nginx sh

# Create django superuser
su-django:
	docker exec -it hockeydb-django python3 manage.py createsuperuser