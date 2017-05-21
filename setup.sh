#!/bin/bash
sudo rm -r /var/www/Apple
IFS=$'\n'
cd ../
sudo cp -r ./Apple /var/www
cd /var/www/Apple
for x in `find ./invoice/static -name '*.js'`; do sudo uglifyjs $x -c -m -o $x; done
for x in `find ./invoice/templates -name '*.html'`; do sudo html-minifier $x -o $x; done
find . -name '*.TTF' -maxdepth 1 -type f -delete
sudo python manage.py collectstatic
cd ../
sudo chown -R www-data:www-data ./Apple
sudo apachectl restart
