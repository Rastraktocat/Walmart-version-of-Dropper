#!/bin/bash

sudo docker stop dropper

sudo docker container prune -f

sudo docker rmi dropper

sudo docker build -t dropper docker_dropper

sudo docker run --name dropper -p 8080:8080 dropper

sudo docker cp dropper:/src/dropper_log.db dropper_log.db

sudo docker rm dropper
