#! /bin/bash

echo -e "\e[1;31m 1. init db \e[0m"
while :; do
    # Wait PostgreSQL
    if python3 manage.py migrate; then
        break
    fi
    sleep 1
done

echo -e "\e[1;31m 2. running \e[0m"
daphne awacs.asgi:application