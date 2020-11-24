#! /bin/bash

echo -e "\e[1;31m 1. collect static \e[0m"
python3 manage.py collectstatic --no-input

echo -e "\e[1;31m 2. init db \e[0m"
while :; do
    # wait postgresql
    if python3 manage.py migrate; then
        break
    fi
    sleep 1
done

echo -e "\e[1;31m 3. dramatiq task \e[0m"
python3 manage.py rundramatiq -p 4 -t 4 --log-file /dev/awacs/logs/dramatiq.log &

echo -e "\e[1;31m 4. apscheduler task \e[0m"
python3 manage.py apscheduler > /dev/awacs/logs/apscheduler.log 2>&1 &

echo -e "\e[1;31m 5. running \e[0m"
daphne -b 0.0.0.0 -p 8002 awacs.asgi:application
