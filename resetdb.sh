#!/bin/sh

sudo -u postgres dropdb iseteam
sudo -u postgres createdb iseteam
python manage.py syncdb --settings iseteam.localsettings
python manage.py runserver --settings iseteam.localsettings
