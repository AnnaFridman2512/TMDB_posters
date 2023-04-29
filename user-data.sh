#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

yum install -y git
git clone https://github.com/AnnaFridman2512/TMDB_posters.git

cd TMDB_posters
docker-compose up -d
