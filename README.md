## Overview:

- A simple project on deploying a 2-tier web application (Flask + MySQL) on an AWS EC2 instance. The deployment is containerized using Docker and Docker Compose. A full CI/CD pipeline is established using Jenkins to automate the build and deployment process whenever new code is pushed to a GitHub repository.

## Step - 1: AWS Configurations

1. AWS EC2 instance setup:
    - In the EC2 console launch an instance.
    - AMI: Ubuntu 24.04 LTS (or the latest available)
    - Select the t2micro or m7iflex.large (the best free tier version available for the region)
    - Create and assign a new key-pair for SSH access.
    - Choose a storage of 20 GB.
2. Configure Security Group:
    - Add the below inbound rules:
    1. Type: SSH, Protocol: TCP, Port: 22, Source: Your IP
    2. Type: HTTP, Protocol: TCP, Port: 80, Source: Anywhere (0.0.0.0/0)
    3. Type: Custom TCP, Protocol: TCP, Port: 5000 (for Flask), Source: Anywhere (0.0.0.0/0)
    4. Type: Custom TCP, Protocol: TCP, Port: 8080 (for Jenkins), Source: Anywhere (0.0.0.0/0)
3. Connect to EC2 instance:
    - Use SSH to connect to the instance's public IP address. (Your public IP address changes when you stop and start your instance. So use the changed IP to again SSH into the instance.)
    - Click on the Connect and copy the SSH command given in the SSH client section.
    - Or you can just simply use:
        
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
    - Retrieve the initial admin password:
    
    ```bash
    sudo cat /var/lib/jenkins/secrets/initialAdminPassword
    ```
    
    - Access the Jenkins dashboard at http://<ec2-public-ip>:8080
    - Paste the password, install suggested plugins, and create an admin user.
5. Grant Jenkins Docker Permissions:
    - This allows Jenkins pipelines to execute Docker commands without using sudo.
    
    ```bash
    sudo usermod -aG docker jenkins
    sudo systemctl restart jenkins
    ```
    

## **Step - 4: GitHub repository configuration**

1. Ensure your GitHub repository contains the following three files at the root level:
    - Jenkinsfile
    - Dockerfile
    - docker-compose.yml

## **Step - 5: Jenkins Pipeline Creation and Execution**

1. Create a new pipeline in the Jenkins, name the project and choose ‘Multibranch pipeline’ or ‘Organisation folder’.
2. Configure the pipeline:
    - Set Definition to Pipeline script from SCM.
    - Choose Git as the SCM and enter your GitHub repo URL.
    - Make sure the script path is ‘Jenkinsfile’ save the configurations.
    - Go to your pipeline and click on ‘Build Now’ to manually run a pipeline to verify if its working.
3. Webhook configuration:
    - Ensure the following plugins are installed:
        - Git
        - GitHub
        - GitHub Branch Source
        - Pipeline
        - Multibranch Pipeline
    - Inside job configuration:
        - Branch Sources → Add Source → GitHub
        - Behaviours **→** Click Add **→** Discover branches
        - Build Triggers **→** Scan Multibranch Pipeline Triggers **→** Check: ****Periodically if not otherwise run
    - Create GitHub webhook:
        - GitHub Repo → Settings → Webhooks → Add Webhook
        
        | Field | Value |
        | --- | --- |
        | Payload URL | [`http://ec2-xx-xx-xx-xx.compute.amazonaws.com:8080/github-webhook/`](http://ec2-xx-xx-xx-xx.compute.amazonaws.com:8080/github-webhook/) |
        | Content type | `application/json` |
        | Secret | (optional but recommended) |
        | Events | Just the push event |

## **Step - 5: Test webhooks and access the app**

- Any git push to the main/dev branch of the configured GitHub repository will automatically trigger the Jenkins pipeline, which will build the new Docker image and deploy the updated application,
- Check for the images and containers using:

```bash
docker images
docker ps
```

- If the containers are up and running, access the app at:
    
    ```bash
    http://<ec2-public-IP>:5000
    ```