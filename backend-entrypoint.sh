#!/bin/bash

./wait-for-it.sh cassandra:9042

python backend/manage.py migrate

python backend/manage.py sync_cassandra

python backend/manage.py runserver 0.0.0.0:9091
