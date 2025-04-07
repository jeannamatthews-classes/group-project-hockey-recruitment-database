FROM python:3.11-alpine
ADD hockeydb ./hockeydb
ADD entrypoint.sh .
ADD manage.py .
ADD requirements.txt .
# Add build dependencies for python mysqlclient
#TODO: Speed up instalation in dev environments by skipping some dependencies
RUN apk add gcc python3-dev musl-dev mariadb-dev mariadb-client
RUN pip install -r requirements.txt                         
EXPOSE 8000/tcp
CMD ["sh","entrypoint.sh"]