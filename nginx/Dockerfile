FROM nginx:mainline-alpine
RUN rm /etc/nginx/conf.d/default.conf
ADD /nginx/hockeydb.conf /etc/nginx/conf.d/default.conf
ADD /django/src/static /srv/static
ADD /django/src/media /srv/media