#! /bin/bash

sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
sudo yum install git -y
git clone https://github.com/AnnaFridman2512/TMDB_posters.git
cd TMDB_posters
sudo docker build -t <your_docker_image_name> .
sudo docker run -p 5000:5000 -d <your_docker_image_name>



