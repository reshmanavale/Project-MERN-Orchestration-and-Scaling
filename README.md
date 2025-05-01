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
 
![Screenshot 2025-04-28 171016](https://github.com/user-attachments/assets/118c9cae-f9a3-4418-ad3f-22c86efef993)

---

## Step 13: Screenshots

**-AWS ECR repo**

![image](https://github.com/user-attachments/assets/7a7ec5bc-33cd-478c-a91e-9894c5bbc8bf)


**-jenkin pipeline execution:**

![image](https://github.com/user-attachments/assets/8072796d-784a-4ecf-bffc-8a0245fda7b3)

**-Python script execution(VPC, subnets, security groups,ASG, ELB)**

![Screenshot 2025-04-28 072305](https://github.com/user-attachments/assets/e38107b4-4c95-4bc6-88e7-ced687b11fa1)
![Screenshot 2025-04-28 072324](https://github.com/user-attachments/assets/7a05a6aa-dcb6-4dcf-89b4-6abfc0e3644b)

**-EKS Cluster:**

![Screenshot 2025-04-28 072355](https://github.com/user-attachments/assets/43bd6c31-2ef5-47a1-94e1-be8cdaf3f68a)

**-Deployment:**
![Screenshot 2025-04-28 070144](https://github.com/user-attachments/assets/b87007a4-94f9-4a05-97bc-f752e9a25f88)

**Frontend:**
![Screenshot 2025-04-28 065232](https://github.com/user-attachments/assets/3d1dda3b-9ef4-41b1-9b9a-92e8e1400ab1)

**Hello-service:**
![Screenshot 2025-04-28 063911](https://github.com/user-attachments/assets/9a76ba94-f839-451e-9890-d5fc97945ca3)

**Profile-service:**
![Screenshot 2025-04-28 060843](https://github.com/user-attachments/assets/26d010a8-1184-4352-a39a-1a9c7b04cf0d)


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
📁 project-root/
│
├── 📁 Boto3-Scripts/                   # Python scripts for automating AWS setup
│   ├── create-listner.py
│   ├── create_target_group.py
│   └── full-infra-setup.py
│
├── 📁 backend/                         # Backend services
│   ├── 📁 helloService/
│   │   ├── Dockerfile
│   │   ├── hello-deployment.yaml
│   │   ├── hello-service.yaml
│   │   ├── index.js
│   │   ├── package.json
│   │   └── package-lock.json
│   │
│   ├── 📁 profileService/
│       ├── Dockerfile
│       ├── profile-deployment.yaml (assumed)
│       ├── profile-service.yaml (assumed)
│       ├── index.js (if exists)
│       ├── package.json
│       └── package-lock.json
│
├── 📁 frontend/                        # Frontend React app
│   ├── 📁 public/
│   ├── 📁 src/
│   ├── Dockerfile
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── package.json
│   ├── package-lock.json
│   └── README.md
│
├── 📁 helm-charts/                     # Helm charts for K8s deployment
│   ├── 📁 frontend/
│   │   ├── 📁 templates/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── .helmignore
│   │   ├── Chart.yaml
│   │   └── values.yaml
│   │
│   ├── 📁 helloService/               (assumed structure)
│   └── 📁 profileService/             (assumed structure)
│
├── 📁 lambda-backup/                  # Lambda function for MongoDB backup
│   └── mongodb_backup_lambda.py
│
├── 📄 Jenkinsfile                     # Jenkins pipeline definition
├── 📄 README.md                       # Project documentation

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

