#! /bin/bash

docker build -t as_nginx ../nginx
docker build -t as_server ../server
docker-compose up -d
