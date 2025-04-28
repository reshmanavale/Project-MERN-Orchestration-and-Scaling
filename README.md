# MERN Application Deployment with AWS, Kubernetes, Jenkins & ChatOps

## 📋 Project Description

This project builds, containerizes, automates, orchestrates, and monitors a full-stack MERN (MongoDB, Express.js, React.js, Node.js) application using AWS Cloud Services, Docker, Kubernetes (EKS), Helm, Jenkins CI/CD, Boto3, Lambda, and ChatOps Integration.

## 🔗 Important Links

- **Project GitHub Link (Fork First):** [SampleMERNwithMicroservices](https://github.com/UnpredictablePrashant/SampleMERNwithMicroservices)
- **How to Pull Updates into Forked Repository:** [Reference Guide](https://stackoverflow.com/questions/3903817/pull-new-updates-from-original-github-repository-into-forked-github-repository)

## 🛠 Jenkins Server Details

- **URL:** [http://3.111.188.91:8080/](http://3.111.188.91:8080/)
- **Username:** `herovired`
- **Password:** `herovired`

# 🚀 Project Execution Steps

## Step 1: Set Up the AWS Environment
- Install AWS CLI and configure credentials.
- Install Boto3:
  ```bash
  pip install boto3
  ```

## Step 2: Prepare the MERN Application
- Fork the GitHub repository.
- Clone your fork:
  ```bash
  git clone https://github.com/<your-username>/SampleMERNwithMicroservices.git
  cd SampleMERNwithMicroservices
  ```
- (Optional) Pull updates from the original repository.
- Ensure Dockerfiles are available for frontend and backend.
- Build Docker Images:
  ```bash
  docker build -t frontend ./frontend
  docker build -t helloservice ./backend/helloservice
  ```

## Step 3: Push Docker Images to Amazon ECR
- Create ECR repositories.
- Authenticate Docker with ECR.
- Tag and push Docker images to ECR.

## Step 4: Version Control
- Create and push the project to AWS CodeCommit (or GitHub if needed).

## Step 5: Continuous Integration with Jenkins
- Install Jenkins on EC2.
- Install necessary plugins (Docker Pipeline, Kubernetes CLI, etc.).
- Create Jenkins Jobs for building and pushing Docker images to ECR.
- Trigger jobs on commits.

## Step 6: Infrastructure as Code (IaC) with Boto3
- Use Boto3 to automate:
  - VPC, Subnets, Security Groups
  - Auto Scaling Groups (ASG)
  - Launch Templates

## Step 7: Deploying Backend Services
- Deploy backend on EC2 with ASG and Docker containers.

## Step 8: Set Up Networking
- Create Elastic Load Balancer (ELB).
- Configure DNS (Route 53).

## Step 9: Deploying Frontend Services
- Deploy frontend containers on EC2.

## Step 10: AWS Lambda Deployment
- Create Lambda Functions:
  - MongoDB database backup to S3 with timestamps.

## Step 11: Kubernetes (EKS) Deployment
- Create EKS Cluster using eksctl.
- Deploy application using Helm charts.

## Step 12: Monitoring and Logging
- Set up monitoring and alerts using CloudWatch.
- Configure logging using CloudWatch Logs.

## Step 13: Documentation
- Document the entire architecture and deployment process.
- Upload documentation to GitHub.

## Step 14: Final Checks
- Validate the MERN application's functionality and availability.

## BONUS Step: ChatOps Integration
- Create SNS Topics.
- Lambda Functions for ChatOps notifications.
- Integrate with Slack/MS Teams/Telegram.

# 📂 Project Folder Structure
```bash
SampleMERNwithMicroservices/
├── backend/
├── frontend/
├── helm/
├── lambda/
├── boto3-scripts/
├── documentation/
└── Jenkinsfile
```

# 🔧 Technologies Used
| Technology | Purpose |
|------------|---------|
| AWS EC2 | Hosting Jenkins, Frontend, Backend |
| AWS ECR | Container Registry |
| AWS EKS | Kubernetes Cluster |
| AWS S3 | MongoDB Backup Storage |
| AWS CloudWatch | Monitoring and Logs |
| AWS Lambda | MongoDB Backup Automation |
| AWS SNS | Deployment Notifications |
| Docker | Containerization |
| Kubernetes | Orchestration |
| Helm | Kubernetes Package Manager |
| Jenkins | CI/CD Pipeline |
| GitHub/CodeCommit | Version Control |
| Boto3 | AWS Resource Automation |

# 🌟 Conclusion
> Successfully deployed a production-ready MERN stack application using modern DevOps and AWS best practices.

# ✨ End of README ✨

