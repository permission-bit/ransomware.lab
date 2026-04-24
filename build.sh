#!/bin/bash
set -e
#build your target folder, subfolder & files 
mkdir ~/Desktop/myapp
echo "Hello World" > ~/Desktop/myapp/test.txt
touch ~/Desktop/myapp/test.pdf
mkdir -p ~/Desktop/myapp/subfolder
echo "sub file" > ~/Desktop/myapp/subfolder/file.txt

rm -rf build dist software.spec

pyinstaller software.py \
  --onedir \
  --windowed \
  --name software \
  --icon icon.icns

plutil -replace LSUIElement -bool true dist/software.app/Contents/Info.plist

#open dist/software.app

