#!/bin/bash
sudo docker run -d --name dropper -p 8080:8080 -v "$(pwd)/dropper_log.txt:$(pwd)/docker_dropper/out/log.txt" dropper

