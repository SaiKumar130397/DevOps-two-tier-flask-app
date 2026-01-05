# DevOps-two-tier-flask-app
## Overview:

- A simple project on deploying a 2-tier web application (Flask + MySQL) on an AWS EC2 instance. The deployment is containerized using Docker and Docker Compose. A full CI/CD pipeline is established using Jenkins to automate the build and deployment process whenever new code is pushed to a GitHub repository.

## Step - 1: AWS Configurations

1. AWS EC2 instance setup:
    1. In the EC2 console launch an instance.
    2. AMI: Ubuntu 24.04 LTS (or the latest available)
    3. Select the t2micro or m7iflex.large (the best free tier version available for the region)
    4. Create and assign a new key-pair for SSH access.
    5. Choose a storage of 20 GB.
2. Configure Security Group:
    - Add the below inbound rules:
    1. Type: SSH, Protocol: TCP, Port: 22, Source: Your IP
    2. Type: HTTP, Protocol: TCP, Port: 80, Source: Anywhere (0.0.0.0/0)
    3. Type: Custom TCP, Protocol: TCP, Port: 5000 (for Flask), Source: Anywhere (0.0.0.0/0)
    4. Type: Custom TCP, Protocol: TCP, Port: 8080 (for Jenkins), Source: Anywhere (0.0.0.0/0)
3. Connect to EC2 instance:
    1. Use SSH to connect to the instance's public IP address.
    2. Click on the Connect and copy the SSH command given in the SSH client section.
    3. Or you can just simply use:
        
        ```bash
        ssh -i /path/to/key.pem ubuntu@<ec2-public-ip>
        ```
        

## Step - 2: Dependancy and tool installations

1. Install Dependecies on EC2:
    1. Update system packages:
        
        ```bash
        sudo apt update && sudo apt upgrade -y
        ```
        
    2. Install git, docker and docker compose:
        
        ```bash
        sudo apt install git [docker.io](http://docker.io/) docker-compose-v2 -y
        ```
        
    3. Start and enable Docker: 
        
        ```bash
        sudo systemctl start docker
        sudo systemctl enable docker
        ```
        
    4. Add User to Docker Group (to run docker without sudo):
        
        ```bash
        sudo usermod -aG docker $USER
        newgrp docker
        ```
        

## Step - 3: Jenkins installation and setup

1. Install Java (OpenJDK 17):
    
    ```bash
    sudo apt install openjdk-17-jdk -y
    ```
    
2. Install Jenkins:
    
    ```bash
    echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
    | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
    sudo apt update
    sudo apt install jenkins -y
    ```
    
3. Start and Enable Jenkins Service:
    
    ```bash
    sudo systemctl start jenkins
    sudo systemctl enable jenkins
    ```
    
4. Initial Jenkins setup:
    1. Retrieve the initial admin password:
        
        ```bash
        sudo cat /var/lib/jenkins/secrets/initialAdminPassword
        ```
        
    2. Access the Jenkins dashboard at http://<ec2-public-ip>:8080
    3. Paste the password, install suggested plugins, and create an admin user.
5. Grant Jenkins Docker Permissions:
    - This allows Jenkins pipelines to execute Docker commands without using sudo.
    
    ```bash
    sudo usermod -aG docker jenkins
    sudo systemctl restart jenkins
    ```
    

## **Step - 4: GitHub repository configuration**

1. Ensure your GitHub repository contains the following three files at the root level:
    1. Dockerfile
    2. docker-compose.yml
    3. Jenkinsfile

## **Step - 5: Jenkins Pipeline Creation and Execution**
  

