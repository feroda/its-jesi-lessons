#!/bin/bash
# render.sh DIR [nome-slide...]: SVG -> PNG 3200x1800
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
dir=$(realpath $1); shift
files=("$@"); [ ${#files[@]} -eq 0 ] && files=($(ls $dir/*.svg))
for svg in "${files[@]}"; do
  png=${svg%.svg}.png
  $CH --headless --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
      --window-size=1600,1100 --default-background-color=00000000 --screenshot=$png "file://$svg" >/dev/null 2>&1
  convert $png -crop 3200x1800+0+0 +repage -background white -alpha remove -alpha off $png
done
