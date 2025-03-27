FROM python:3.11-alpine
ADD src/ .
RUN pip install -r requirements.txt
RUN python3 manage.py migrate
EXPOSE 8000
CMD ["python3","manage.py","runserver"]