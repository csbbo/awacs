FROM openresty/openresty:1.15.8.2-7-bionic-nosse42
ADD . /web/nginx
WORKDIR /web
ENV LUA_CPATH=/web/nginx/libinjection/?.so;;
ENV LUA_PATH=/web/nginx/libinjection/?.lua;;
RUN mkdir /web/nginx/logs
CMD /usr/local/openresty/bin/openresty -p /web/nginx/ -c nginx.conf