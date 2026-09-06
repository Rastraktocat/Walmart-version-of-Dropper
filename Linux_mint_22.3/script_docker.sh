#!/bin/bash

sudo docker stop dropper

sudo docker container prune -f

sudo docker rmi dropper

sudo docker build -t dropper docker_dropper

sudo docker run --name dropper -p 8080:8080 -v "$(pwd)/dropper_log.txt/:$(pwd)/docker_dropper/src/out/log.txt" dropper
