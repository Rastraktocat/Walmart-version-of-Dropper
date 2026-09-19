#!/bin/bash

sudo docker stop dropper

sudo docker container prune -f

sudo docker rmi dropper

sudo docker build -t dropper docker_dropper

outer=${PWD}/dropper_log.db

inner=${PWD}/docker_dropper/src/dropper_log.db

sudo docker run --rm --name dropper -p 8080:8080 --mount type=bind,target="${inner}",source="${outer}" dropper
