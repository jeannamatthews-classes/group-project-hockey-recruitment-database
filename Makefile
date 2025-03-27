build:
	docker build -t hockey-db .

run:
	docker run -p 8000:8000 hockey-db