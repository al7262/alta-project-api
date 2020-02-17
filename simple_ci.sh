#!/bin/bash

# Push from local
sudo docker rmi garryarielcussoy/easykachin:be
sudo docker build -t garryarielcussoy/easykachin:be .
sudo docker push garryarielcussoy/easykachin:be