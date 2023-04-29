#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

mkdir /app
cd /app
curl -LJO https://raw.githubusercontent.com/AnnaFridman2512/TMDB_posters/main/docker-compose.yml

docker-compose up -d
