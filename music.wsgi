#!/usr/bin/python3
import sys
sys.stdout = sys.stderr

sys.path.insert(0,'/var/www/music')

from app import app as application
