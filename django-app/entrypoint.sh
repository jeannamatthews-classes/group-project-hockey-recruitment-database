#!/bin/sh

if [ "$HOCKEYDB_BUILD_MODE" = "PROD" ]; then
    # alpine uses mariadb-admin, it is functionaly equivalent to mysqladmin
    until mariadb-admin ping --host hockeydb-mysql --skip-ssl --silent
    do
        sleep 1
        echo "Waiting for mysql"
    done
fi

# Check for any unapplied migrations and ensure the database schema is up to date
python3 manage.py makemigrations hockeydb
python3 manage.py migrate  

# Collect static files into the volume
python3 manage.py collectstatic --noinput 

# Run the server, passing signals down so that the container dies properly
python3 manage.py runserver 0.0.0.0:8000 & pid=$!
wait $pid