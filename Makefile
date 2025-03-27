# (Re-)build and run the current stack
build-dev:
	echo "Building and running development stack"
	docker compose -f docker-compose.dev.yaml up --build

# Run the current stack without rebuilding, using the last built version
run-dev:
	echo "Building and running development stack"
	docker compose -f docker-compose.dev.yaml up

# (Re-)build and run a production-ready stack
build-prod:
	echo "Not implemented yet!"

# Run the production-ready stack without rebuilding, using the last built version
build-prod:
	echo "Not implemented yet!"