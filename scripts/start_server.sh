#!/bin/bash

# get all the variables
APPLICATION_NAME="univ"
DESTINATION_PATH="/home/ubuntu/python/"

# go to the application folder
cd $DESTINATION_PATH

source bit_talk/bin/activate

#pm2 start scripts/start.sh --name PYTHON 
python manage.py runserver 0.0.0.0:8000 &
# and (re)start forever
#ps ax | grep -v grep | grep pm2 > /dev/null
#if [ $? != 0 ]; then
    #/opt/bitnami/node/bin/pm2 restart 0
#else
    #/opt/bitnami/node/binpm2 start run-server.js --name=univ
#fi
