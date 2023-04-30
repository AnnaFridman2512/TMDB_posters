#!/bin/bash

# Update the system packages
sudo yum update -y

# Install Python 3 and pip3
sudo yum install python3 python3-pip -y

# Install additional development libraries required by some Python packages
sudo yum install gcc python3-devel openssl-devel -y

# Install Git
sudo yum install git -y

# Install Docker
sudo amazon-linux-extras install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone the repository and install the dependencies
git clone https://github.com/AnnaFridman2512/TMDB_posters.git /TMDB_posters
cd /TMDB_posters
sudo pip3 install -r requirements.txt

# Start the application using Docker Compose
sudo docker-compose up -d
