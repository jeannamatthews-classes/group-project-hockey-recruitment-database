# Hockey DB Deployment Guide
## Before You Begin
For easy deployment, the Hockey DB server runs on docker. This guide expects some familiarity with servers and networking, and is targeted towards an entry to mid-level systems administrator. The exact steps for the following items will differ between IT environments, so they will be left to the discression of the installer.
### Hardware Requirements
- A linux server, either a VM or bare metal
- At least 4 CPU cores
- At least 8GB RAM
- A network connection
### Deployment Environment
The Hockey DB server is a web service, which means that any clients who wish to use it will need to be able to access it over the network. We would **strongly reccomend** a static IP address and a DNS name for the server. Additionaly, since this program is not intended to be generally accessible to the public, we would reccomend placing it on your intranet behind a VPN.
### Security
No part of the Hockey DB server should be considered secure in it's default configuration. It is ultimatley up to the installer to ensure that proper security considerations are taken to protect the server. We would **strongly** reccomend against exposing the server to the open internet. By default, the Hockey DB server uses **insecure** HTTP on port 80 and does not provide any access control mechanisms. If you are comfortable doing so, you can edit the nginx configuration to support HTTPS with an SSL certificate, or you could place it behind your own reverse proxy which provides this functionality. Additionaly, we reccomend applying access control at the reverse proxy. Many plugins exist for nginx and other reverse proxies to connect into different directory systems such as LDAP and OpenID. For added protection, the Hockey DB server should be deployed behind a VPN or on a secure intranet. You should not rely on obscurity to secure your server instance. If your server is left with no access control, someone **will** find it and it **will** be exploited.

## Installation
Once you've completed the prerequisite steps above, you can begin the installation process for the Hockey DB server.
### Install Docker
Install docker engine from their guide at https://docs.docker.com/engine/install/. The installation process for every linux distribution is slightly different, so it will not be covered here. In general, you should install docker directly from docker instead of your distribution's sources, as they are often outdated.
### Clone the Repository
Clone this git repository to your server. You should choose the install location as you see fit based on your organization's prefrences. If you don't have any preference for where you install the program, we reccomend `/docker/hockeydb` or `/opt/hockeydb`, the latter of which is reccomended as per the [FHS](https://refspecs.linuxfoundation.org/fhs.shtml). Where you install the server is largely unimportant and left to the installer's discression.
### Configure Settings
Open `docker-compose.prod.yaml` with your text editor of choice, and edit any lines which are marked with a comment. Of primary note are `HOCKEYDB_SECRET_KEY`, `HOCKEYDB_DB_PASSWORD`, `MYSQL_PASSWORD`, and `MYSQL_ROOT_PASSWORD`. We strongly reccomend setting these to random values. On most linux distributions, you can easily generate a secure random password using `openssl rand -base64 32`. You should generate a new password for each of these fields. You should also set `HOCKEYDB_ALLOWED_HOSTS` to the DNS name that your server will be accessible at. If you do not set properly, the backend will reject all connections as a security policy.
### Start the Server
Now its time to start the server. First make sure that the docker daemon is running. The way you do this will vary depending on your linux distribution. Then, as a user authorized to access the docker daemon, run `make prod` to start the server. As long as no errors are thrown during the startup, you should be able to run `docker ps` and see that all the containers are now running.
### Test
Your server should now be running and accessible over the network. You should be able to go to the DNS name you gave the server and see the main page for the program. If for some reason it isn't working, retrace your steps and make sure you configured everything properly. 
### Finalize Your Installation
Congratulations, you've now finished the installation process. We reccomend taking the following steps to ensure smooth operation of your Hockey DB server:
- Use a service file or other means to automatically run the Hockey DB server whenever your server restarts.
- Secure your installation behind an authentication service.
- Test that there is some way to access the server from outside your network.
- Ensure your installation stays up to date by checking the repository for commits and running `git pull` to fetch the latest changes.