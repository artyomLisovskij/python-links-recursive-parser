# Python crawler that fetch all links on the website recursively 
Docker-based crawler that recursively find all links on your page, fetch page by every link, find all links, ... till all of the links will not be added to redis and fetched.

# getting started
We use:
- docker-compose
- redis
- python3
- beautifulsoup4

Links contains vk.com, instagram.com, facebook.com, twitter.com will not be fetched.

Fast start:
- change START_URL in docker-compose.yaml
- run script by docker-compose up --build

We use redis as db, so if script failed you can continue parsing.

Result will be printed to docker console as list of links when all links will fetched.
