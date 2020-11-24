#!/bin/sh
python2.7 -m SimpleHTTPServer 9191 & 
xdg-open http://localhost:9191
