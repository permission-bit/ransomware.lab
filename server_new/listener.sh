#!/bin/bash

META_PORT="9001"
DATA_PORT="9000"

SAVE_DIR="$HOME/incoming_chunks"

mkdir -p "$SAVE_DIR"

while true; do
    CHUNK_NAME=$(nc -l "$META_PORT")

    if [ -z "$CHUNK_NAME" ]; then
        continue
    fi

    nc -l "$DATA_PORT" > "$SAVE_DIR/$CHUNK_NAME"
done