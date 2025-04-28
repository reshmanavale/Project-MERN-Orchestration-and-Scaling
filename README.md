# MERN Application Orchestration and Scaling Project

---

## Project Description

This project demonstrates a full DevOps pipeline to build, deploy, orchestrate, and monitor a containerized **MERN** (MongoDB, Express.js, React.js, Node.js) application on AWS Cloud infrastructure using modern DevOps practices.

- **CI/CD** with Jenkins
- **Containerization** with Docker
- **Orchestration** with Kubernetes (EKS)
- **Infrastructure as Code** with Boto3
- **Monitoring** with CloudWatch
- **Backup Automation** with Lambda
- **ChatOps Integration** with SNS and Slack/MS Teams

---

## Project Repository

- Forked Project Link: [SampleMERNwithMicroservices](https://github.com/UnpredictablePrashant/SampleMERNwithMicroservices)
- Update Fork Regularly: [Guide to Update Fork](https://stackoverflow.com/questions/3903817/pull-new-updates-from-original-github-repository-into-forked-github-repository)

---

## Jenkins Credentials

- **Jenkins URL**: http://3.111.188.91:8080/
- **Username**: herovired
- **Password**: herovired

---

# Step-by-Step Project Execution

## Step 1: Set Up the AWS Environment

**Install AWS CLI:**
```bash
sudo apt update
sudo apt install awscli -y
```

**Configure AWS CLI:**
```bash
aws configure
```
(Provide Access Key, Secret Key, Region, and output format)

**Install Boto3:**
```bash
pip install boto3
```

---

## Step 2: Prepare the MERN Application

**Clone the Repository:**
```bash
git clone https://github.com/<your-username>/SampleMERNwithMicroservices.git
cd SampleMERNwithMicroservices
```

**Sample Dockerfile for Frontend:**
```Dockerfile
FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

**Authenticate Docker to ECR:**
```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

**Push Docker Image to ECR:**
```bash
docker build -t frontend .
docker tag frontend:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/frontend

docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/frontend
```

---

## Step 3: Version Control with AWS CodeCommit (Optional)

**Push Code to CodeCommit:**
```bash
git remote add codecommit https://git-codecommit.<region>.amazonaws.com/v1/repos/<repo-name>
git push codecommit main
```

(If CodeCommit not accessible, continue using GitHub)

---

## Step 4: Continuous Integration with Jenkins

**Install Jenkins Plugins:** Docker, Git, ECR, Kubernetes CLI, AWS CLI.

**Create Jenkins Pipeline Job:**

**Sample Jenkinsfile:**
```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/<your-username>/SampleMERNwithMicroservices.git'
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t frontend .' 
            }
        }
        stage('Push to ECR') {
            steps {
                sh 'docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/frontend'
            }
        }
    }
}
```

---

## Step 5: Infrastructure as Code (IaC) with Boto3

**Create VPC, Subnet, and EC2 using Boto3:**
```python
import boto3

ec2 = boto3.client('ec2')
response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc_id = response['Vpc']['VpcId']
```

(Create Security Groups, Launch Templates, ASG similarly)

---

## Step 6: Deploy Backend Services

**Sample User Data for Backend EC2 Instances:**
```bash
#!/bin/bash
yum update -y
yum install docker -y
service docker start
docker run -d -p 5000:5000 <aws_account_id>.dkr.ecr.<region>.amazonaws.com/backend
```

---

## Step 7: Set Up Networking

**Create Load Balancer Using AWS CLI:**
```bash
aws elbv2 create-load-balancer --name backend-lb --subnets subnet-xxxx subnet-yyyy --security-groups sg-xxxx --scheme internet-facing --type application
```

**Configure Target Groups and Listeners.**

---

## Step 8: Deploy Frontend Services

Same approach as backend, deploy frontend instances and containers.

---

## Step 9: AWS Lambda Deployment

**Sample Lambda Code to Backup MongoDB:**
```python
import boto3
import datetime
import subprocess

def lambda_handler(event, context):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = f'/tmp/backup_{timestamp}.gz'
    subprocess.run(['mongodump', '--uri', 'mongodb+srv://user:password@cluster', '--archive='+backup_file, '--gzip'])
    s3 = boto3.client('s3')
    s3.upload_file(backup_file, 'my-backup-bucket', 'backup_'+timestamp+'.gz')
```

Package with `pymongo` if needed.

---

## Step 10: Kubernetes (EKS) Deployment

**Create EKS Cluster:**
```bash
eksctl create cluster --name mern-cluster --region <region> --nodegroup-name standard-workers --node-type t3.medium --nodes 3
```

**Deploy Helm Charts:**
```bash
helm install backend ./backend-chart/
helm install frontend ./frontend-chart/
```

---

## Step 11: Monitoring and Logging

**Enable CloudWatch Container Insights:**
```bash
aws eks update-cluster-config --name mern-cluster --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
```

Install CloudWatch Agent as DaemonSet if needed.

---

## Step 12: Documentation

 **Architecture Diagram**
 

---

## Step 13: Screenshots

---

## Step 14: Final Checks

- Access Load Balancer URL.
- Test all microservices.
- Validate Frontend-Backend Integration.

---

## BONUS: ChatOps Integration

**Create SNS Topic:**
```bash
aws sns create-topic --name deployment-alerts
```

**Sample Lambda to Send Slack Message:**
```python
import requests

def lambda_handler(event, context):
    webhook_url = 'https://hooks.slack.com/services/TXXXX/BXXXX/XXXX'
    message = {'text': "Deployment succeeded!"}
    requests.post(webhook_url, json=message)
```

**SES Setup:** Verify emails and configure notification rules.

---

# Project File Structure (Sample)

```
📁 project-root
├── 📁 backend
│   ├── 📄 Dockerfile
│   ├── 📄 deployment.yaml
├── 📁 frontend
│   ├── 📄 Dockerfile
│   ├── 📄 deployment.yaml
├── 📁 jenkins
│   ├── 📄 frontend-pipeline.groovy
│   ├── 📄 backend-pipeline.groovy
├── 📁 terraform (optional)
├── 📁 boto3-scripts
│   ├── 📄 create_infra.py
│   ├── 📄 create_lambda.py
├── 📁 lambda
│   ├── 📄 mongodb_backup_lambda.py
├── 📄 eksctl-cluster.yaml
├── 📄 README.md
```

---

# Conclusion

✅ Successfully deployed a highly available, containerized MERN Application.
✅ Achieved end-to-end DevOps Pipeline with AWS ecosystem.
✅ Integrated Monitoring, Logging, Backup, and ChatOps Notification.

---

# 📌 Notes

- Replace placeholders with your actual AWS IDs, ECR repo names, Load Balancer URLs.
- Attach screenshots at every important step.
- Monitor resource usage to avoid unexpected AWS billing.

---

# Thank you 🙌

Feel free to enhance this by adding GitOps or microservice auto-scaling next!

