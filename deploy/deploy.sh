#! /bin/bash

docker build -t as_openresty ../openresty
docker build -t as_server ../server
docker-compose up -d
