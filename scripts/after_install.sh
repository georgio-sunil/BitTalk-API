#!/bin/bash

# get all the variables
APPLICATION_NAME="univ"
DESTINATION_PATH="/home/ubuntu/python"
# create /server/uploads if it doesn't exist

# create /webapps/logs if it doesn't exist

# copy certs if they don't exist
cd $DESTINATION_PATH

if [ ! -d bit_talk ]
then
    virtualenv bit_talk
    source bit_talk/bin/activate
    pip install -r requirements.txt
else
    source bit_talk/bin/activate
fi
if [ ! -d logs ]
then
    mkdir logs
fi

