FROM python:3.11-alpine
ADD src/ .
ADD entrypoint.sh .
# Add build dependencies for python mysqlclient
RUN apk add gcc python3-dev musl-dev mariadb-dev mariadb-client
RUN pip install -r requirements.txt                         
EXPOSE 8000/tcp
CMD ["sh","entrypoint.sh"]