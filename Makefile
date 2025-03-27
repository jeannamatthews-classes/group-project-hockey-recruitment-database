# (Re-)build and run the current stack
build-dev:
	echo "Building and running development stack"
	docker compose -f docker-compose.dev.yaml up --build

# Run the current stack without rebuilding, using the last built version
run-dev:
	echo "Running development stack"
	docker compose -f docker-compose.dev.yaml up

# (Re-)build and run a production-ready stack
build-prod:
	echo "Building and running production stack"
	docker compose -f docker-compose.prod.yaml up --build

# Run the production-ready stack without rebuilding, using the last built version
run-prod:
	echo "Running production stack"
	docker compose -f docker-compose.dev.yaml up

# Remove existing containers
clean:
	docker compose -f docker-compose.dev.yaml rm -f
	docker compose -f docker-compose.prod.yaml rm -f