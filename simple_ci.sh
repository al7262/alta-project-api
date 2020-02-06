#!/bin/bash

# Push from local
sudo docker rmi garryarielcussoy/easykachin:be
alta123
sudo docker build -t garryarielcussoy/easykachin:be .
sudo docker push garryarielcussoy/easykachin:be

# Go to server
cd ~/Downloads
ssh -i alta-deployment.pem admin@13.229.61.125
sh short.sh
logout