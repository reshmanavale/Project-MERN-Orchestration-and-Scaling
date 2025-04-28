# Project: MERN Application Orchestration and Scaling on AWS EKS

---

## Overview
This project demonstrates how to deploy a **MERN-based Microservices Application** on an AWS EKS Cluster, using **Helm charts**, **LoadBalancer services**, **AWS Lambda for MongoDB backup**, **basic monitoring**, and **CI/CD pipeline setup with Jenkins**.

We have split the MERN app into multiple services:
- **Profile Service**
- **Hello Service**
- **Frontend Service**


---

# Project Steps

## Step 1: Initial Setup
- **AWS CLI** and **kubectl** installed.
- **IAM Role** with necessary permissions.
- **ECR** repository created for Docker images.
- **Jenkins Server** set up (EC2) for CI/CD (details below).


## Step 2: Create EKS Cluster
- Used **eksctl** to create a basic EKS cluster.
- Verified cluster access:
```bash
aws eks --region <region> update-kubeconfig --name <cluster-name>
kubectl get nodes
```

---

## Step 3: Dockerize Application
- Dockerized all microservices (Profile, Hello, Frontend).
- Pushed Docker images to AWS **ECR**.


---

## Step 4: Deploy with Kubernetes YAMLs
- Created Kubernetes `deployment.yaml` and `service.yaml` for each microservice.
- Exposed **Frontend** and **Profile** via **LoadBalancer**.

#### Example Folder Structure:
```
Project-MERN-Orchestration-and-Scaling/
    backend/
        helloService/
        profileService/
    frontend/
    helm-charts/
```


---

## Step 5: Move to Helm Chart
- Created individual Helm charts for each service (`helloService`, `profileService`, `frontendService`).
- Common files inside each chart:
  - Chart.yaml
  - values.yaml
  - templates/
    - deployment.yaml
    - service.yaml

#### Important:
- Updated `service.type` to **LoadBalancer** where external exposure was needed.
- Managed MongoDB URI with **ConfigMap** (not hardcoded).


---

## Step 6: MongoDB Connection Fix
- Issue: `MongoRuntimeError: Unable to parse <mongo-host>`
- Solution: Properly passed `MONGO_URL` environment variable inside Kubernetes Deployment.

---

## Step 7: AWS Lambda for MongoDB Backup
- Wrote a basic Python Lambda using `boto3` and `pymongo`.
- Bundled dependencies and function code as a ZIP.
- Deployed on AWS Console manually.

#### Lambda Key Points:
- Scheduled (can use EventBridge later).
- Backs up MongoDB and stores backup in an S3 bucket.

#### How to Create Lambda ZIP (Windows):
```bash
mkdir mylambda
cd mylambda
pip install pymongo -t .
copy lambda_function.py .
powershell Compress-Archive * ../lambda-package.zip
```


---

## Step 8: Jenkins Pipeline for ECR Build and Deployment
- Installed Jenkins on EC2.
- Installed Docker, kubectl, awscli on Jenkins server.
- Created simple Jenkins pipeline:
  - Build Docker images
  - Push to ECR
  - Deploy updated images to EKS

> (Sample `Jenkinsfile` to be provided if needed)

---

## Step 9: Basic Monitoring (Optional)
- Plan to integrate CloudWatch Logs agent into EKS.
- (Skipped due to IAM restrictions.)
- Future Scope: Use Prometheus + Grafana via Helm charts.


---

# Challenges Faced

| Stage | Issue | Solution |
|:-----|:-----|:-----|
| EKS Cluster Creation | Slow cluster provisioning | Waited patiently; verified using `eksctl get cluster` |
| MongoDB Connection | `Unable to parse <mongo-host>` | Added proper env variable `MONGO_URL` |
| Helm Migration | Service not reachable | Changed service type from `ClusterIP` to `LoadBalancer` |
| Lambda Deployment | `No module named pymongo` error | Uploaded packaged zip with dependencies |
| Helm Install | Resource already exists error | Deleted old deployments/services before Helm install |


---

# Final Folder Structure
```
Project-MERN-Orchestration-and-Scaling/
|
|-- backend/
|   |-- helloService/ (NodeJS)
|   |-- profileService/ (NodeJS)
|
|-- frontend/
|   |-- (ReactJS app)
|
|-- helm-charts/
|   |-- helloService/
|   |-- profileService/
|   |-- frontendService/
|
|-- lambda/
|   |-- lambda_function.py
|   |-- requirements.txt
|   |-- (lambda-package.zip)
|
|-- Jenkins/
|   |-- Jenkinsfile
```


---

# Screenshots to Add

- EKS cluster creation complete (AWS Console)
- Successful `kubectl get svc` showing LoadBalancer
- Helm install output
- Lambda function creation
- Jenkins pipeline successful build
- Browser Access to Frontend LoadBalancer URL


---

# Conclusion
This project successfully demonstrates how to deploy and scale a containerized MERN microservice application on AWS EKS using Helm charts, manage backups using Lambda functions, and basic CI/CD setup with Jenkins.

Future Enhancements:
- Full Monitoring using Prometheus + Grafana.
- Auto-healing setup.
- Advanced Logging with Fluentd/CloudWatch agent.

---

# (END)

---

*Note: You can directly copy this and modify with your actual LoadBalancer URLs, IP addresses, cluster names, and screenshots.*

Would you like me to also quickly prepare a sample `Jenkinsfile`?

