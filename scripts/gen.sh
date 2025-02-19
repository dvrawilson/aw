#!/bin/sh
rm ../www/xarchives.html && ./munge.sh && ./xarchives.py > ../www/xarchives.html
