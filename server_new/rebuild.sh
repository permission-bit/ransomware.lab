#!/bin/bash

cd "$HOME/incoming_chunks" || exit 1

cat backup.part_* > backup.tar.gz

tar -tzf backup.tar.gz >/dev/null 2>&1 || exit 1

mkdir -p restored
tar -xzf backup.tar.gz -C restored