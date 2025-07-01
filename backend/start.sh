#!/bin/sh

port=$2
if [ "$port" = "" ]; then
  port=8101
fi

if [ $1 = "app" ]; then
    echo "start app"
    /usr/local/bin/python -m granian --interface asgi main:app --workers 2 --bind 0.0.0.0:$port
fi

if [ $1 = "celery-worker" ]; then
    echo "start celery worker"
     /usr/local/bin/python -m celery -A celery_worker.worker.celery worker -l INFO
fi

if [ $1 = "celery-beat" ]; then
    echo "start celery beat"
    /usr/local/bin/python  -m celery -A celery_worker.worker.celery beat -S celery_worker.scheduler.schedulers:DatabaseScheduler -l INFO
fi