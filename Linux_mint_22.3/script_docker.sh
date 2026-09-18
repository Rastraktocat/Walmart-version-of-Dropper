#!/bin/bash

sudo docker stop dropper

sudo docker container prune -f

sudo docker rmi dropper

sudo docker build -t dropper docker_dropper

sudo docker run --rm --name dropper -p 8080:8080 --mount type=bind, source="$pwd/docker_dropper/src/dropper_log.db", target="$pwd/dropper_log.db" dropper
