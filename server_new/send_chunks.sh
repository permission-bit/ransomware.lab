#!/bin/bash

SERVER_IP="YOUR_SERVER_IP"
META_PORT="9001"
DATA_PORT="9000"

WORK_DIR="$HOME/.backup_chunks"
ARCHIVE="$WORK_DIR/backup.tar.gz"
CHUNK_DIR="$WORK_DIR/chunks"
STATE_FILE="$WORK_DIR/sent_chunks.txt"

CHUNK_SIZE="5m"
MAX_RETRIES=5
RETRY_DELAY=5

PATHS=(
    "$HOME/Desktop/myapp"
    "$HOME/Documents/projects"
    "$HOME/Downloads/test.txt"
)

mkdir -p "$WORK_DIR" "$CHUNK_DIR"
touch "$STATE_FILE"

# Archiv nur erstellen, wenn es noch nicht existiert
if [ ! -f "$ARCHIVE" ]; then
    tar -czf "$ARCHIVE" "${PATHS[@]}" 2>/dev/null
fi

# Chunks nur erstellen, wenn noch keine existieren
if [ -z "$(ls -A "$CHUNK_DIR" 2>/dev/null)" ]; then
    split -b "$CHUNK_SIZE" "$ARCHIVE" "$CHUNK_DIR/backup.part_"
fi

for CHUNK in "$CHUNK_DIR"/backup.part_*; do
    CHUNK_NAME=$(basename "$CHUNK")

    # schon gesendet? dann überspringen
    if grep -Fxq "$CHUNK_NAME" "$STATE_FILE"; then
        continue
    fi

    COUNT=0

    until {
        echo "$CHUNK_NAME" | nc "$SERVER_IP" "$META_PORT"
        sleep 1
        nc "$SERVER_IP" "$DATA_PORT" < "$CHUNK"
    }
    do
        COUNT=$((COUNT + 1))

        if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
            exit 1
        fi

        sleep "$RETRY_DELAY"
    done

    # Chunk als erledigt speichern
    echo "$CHUNK_NAME" >> "$STATE_FILE"
done

exit 0