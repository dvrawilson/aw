#!/bin/sh
rm ../docs/xarchives.html && ./munge.sh && ./xarchives.py > ../docs/xarchives.html
