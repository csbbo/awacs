FROM ubuntu:20.04

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
    && apt-get install -y python3.8 python3.8-dev python3-pip \
    && pip3 install -r /tmp/requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple/ \
    && ln -sfv /web/awacs/settings.py.pro /web/awacs/settings.py

ADD ./src/awacs /web

WORKDIR /web

CMD bash /web/run.sh
