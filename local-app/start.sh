#!/bin/sh
python2.7 -m SimpleHTTPServer 7777 & 
xdg-open http://localhost:7777
