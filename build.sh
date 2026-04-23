#!/bin/bash
set -e

rm -rf build dist software.spec

pyinstaller software.py \
  --onedir \
  --windowed \
  --name software \
  --icon icon.icns

plutil -replace LSUIElement -bool true dist/software.app/Contents/Info.plist

#open dist/software.app

