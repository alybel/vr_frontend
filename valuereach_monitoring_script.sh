#!/bin/bash

DATE=`date +%c`;
ME=`basename "$0"`;
LCK="./${ME}.LCK";
exec 8>$LCK;

if flock -n -x 8; then
  echo ""
  echo "Starting your script..."
  echo ""

  PYTHONPATH=/home/matyas/vr_frontend uwsgi --http :15000 --wsgi-file /home/matyas/vr_frontend/wsgi.py --callable application

  echo ""
  echo "Script started  $DATE";
  echo "Script finished `date +%c`";
else
  echo "Script NOT started - previous one still running at $DATE";
fi
