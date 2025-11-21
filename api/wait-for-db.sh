#!/bin/sh
until nc -z db 3306; do
  echo "Waiting for database..."
  sleep 1
done
exec "$@"
