#!/bin/bash

# get all the variables
APPLICATION_NAME="univ"
DESTINATION_PATH="/home/ubuntu/python/"

# go to the application folder
cd $DESTINATION_PATH

pkill -9 python
#pm2 stop 0
#pm2 delete 0
# pm2 save
