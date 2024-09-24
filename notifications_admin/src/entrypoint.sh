#!/bin/sh

python3 -m alembic upgrade head
python3 -m gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000