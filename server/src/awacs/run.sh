#! /bin/bash

echo -e "\e[1;31m 1. init db \e[0m"
while :; do
    # Wait PostgreSQL
    sleep 3
    if python3 manage.py migrate; then
        break
    fi
done

echo -e "\e[1;31m 2. collect static \e[0m"
python3 manage.py collectstatic --no-input

echo -e "\e[1;31m 3. running \e[0m"
daphne -b 0.0.0.0 -p 8002 awacs.asgi:application
