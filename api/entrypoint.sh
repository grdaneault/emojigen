#!/usr/bin/env sh
uwsgi --http-socket 0.0.0.0:5000 --module wsgi:app --enable-threads
