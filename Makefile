build:
	docker build -t hockey-db .

run: build
	docker run -P hockey-db