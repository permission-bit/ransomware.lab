#!/bin/bash

FILE_NAME=$(nc -l 9001)

echo "listener is listening on port 9000"

echo "[+] Incoming file: $FILE_NAME"

mkdir -p uploads

nc -l 9000 > "uploads/$FILE_NAME"

echo "[+] Saved as: uploads/$FILE_NAME"