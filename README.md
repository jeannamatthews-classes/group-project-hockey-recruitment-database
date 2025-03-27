# Hockey-Recruiting-Database

description TODO

# Docker
Docker support is in progress. I currently have a basic dockerfile that _should_ be working, but I'm having port forwarding issues. I think it's specificaly a mac problem, but I haven't tested on another device yet. Docker should make managing dependencies and whatnot easier by containerizing the app.

# Running
- Instructions for Linux/macOS users
### Create virtual environment
start with the root of the repository as your working directory
```commandline
python3 -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt
```

### Set up local database
if you are using the default sqlite3 database, you can set it up with
```commandline
python3 src/manage.py migrate
```
The data will be stored in the db.sqlite3 file

### Run the server
With the virtual environment activated:
```commandline
python3 src/manage.py runserver
```
This should start the server on localhost, which you can visit with the link it prints out
