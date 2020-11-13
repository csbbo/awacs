#! /bin/bash

docker build -t as_openresty ../openresty
docker build -t as_server ../server
cp -rf ../data .
docker-compose up -d