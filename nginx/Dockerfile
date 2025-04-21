FROM nginx:mainline-alpine

# install needed packages
RUN apk add --no-cache npm

# configure nginx
RUN rm /etc/nginx/conf.d/default.conf
ADD /nginx/hockeydb.conf /etc/nginx/conf.d/default.conf

# build frontend
ADD /frontend /app
WORKDIR /app
RUN npm install
RUN npm run build
RUN mv /app/dist/* /usr/share/nginx/html
RUN rm -rf /app
