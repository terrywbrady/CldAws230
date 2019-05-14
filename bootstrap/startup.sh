# Update OS software
sudo -n yum -y update

# Install Java 8
sudo -n yum -y install java-1.8.0-openjdk-devel
sudo -n yum -y remove java-1.7.0-openjdk

# Install Git
sudo -n yum -y install git

# install docker
sudo yum install docker -y

# Start the Docker Service
sudo service docker start

# Add the ec2-user to the docker group so you can execute Docker commands without using sudo.
sudo usermod -a -G docker ec2-user

# Install Docker compose
# https://docs.docker.com/compose/install/

sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod 755 /usr/local/bin/docker-compose

# Clone DSpace-Docker-Images
sudo su -l ec2-user -c "cd;git clone https://github.com/DSpace-Labs/DSpace-Docker-Images.git;cd DSpace-Docker-Images/docker-compose-files/dspace-compose;docker-compose -p d6 -f docker-compose.yml -f d6.override.yml up -d"
