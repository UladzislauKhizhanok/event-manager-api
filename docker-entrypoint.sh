#!/bin/sh

set -e

ACTION=""
if [ $# -ge 1 ]; then
  ACTION=${1} ; shift
fi

case "${ACTION}" in

  ''|-*) # Default for server up
    python manage.py migrate
    exec gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 4 app.wsgi:application
    ;;

  test)
    exec python manage.py test
    ;;

  *) # For script running
    exec ${ACTION} ${@}
    ;;
esac
