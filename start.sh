#!/bin/bash
xdpyinfo | grep dots
xrandr --dpi 96
cd $(dirname $0)
killall conky
mkdir -p ~/.fonts
cp fonts/*.*tf ~/.fonts > /dev/null 2>&1
mkdir -p ~/.local/share/fonts/
cp fonts/*.*tf ~/.local/share/fonts/ > /dev/null 2>&1
fc-cache ~/.fonts
python info01.py
python clock01.py
python mem01.py
python cpu01.py
python disk01.py
python top01.py
python net01.py
#python graphiccard01.py
conky -q -c infofile
conky -q -c clockfile
conky -q -c memfile
conky -q -c cpufile
conky -q -c topfile
#conky -q -c diskfile
conky -q -c netfile
python poll_disk.py &
python poll_day.py &
notify-send -i ./AutomatiK.png \
"Information" \
"Automatik is started
To move the widgets around the desktop,
use Alt+ left-Click"
