#! /bin/bash

docker-compose down
docker image rm as_nginx as_server

bash deploy.sh