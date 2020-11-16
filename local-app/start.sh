#!/bin/sh
python2.7 -m SimpleHTTPServer 8989 & 
xdg-open http://localhost:8989
