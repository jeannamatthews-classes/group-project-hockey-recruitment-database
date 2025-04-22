#!/bin/sh
# Must be run from this directory on a freshly initialized database

sudo sqlite3 ../data/db.sqlite3 < demo_data.sql