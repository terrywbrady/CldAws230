#!/bin/sh
sudo su -l ec2-user -c "cd;cd DSpace-Docker-Images;git pull origin;cd docker-compose-files/dspace-compose;docker-compose -p d6 -f docker-compose.yml -f d6.override.yml down;docker-compose -p d6 -f docker-compose.yml -f d6.override.yml up -d"
