pipeline {
    agent any

    environment {
        AWS_REGION = 'us-west-1'
        ECR_REGISTRY = '975050024946.dkr.ecr.us-west-1.amazonaws.com'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/reshmanavale/Project-MERN-Orchestration-and-Scaling.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Build all services
                    sh '''
                    docker build -t hello-service ./backend/hello-service
                    docker build -t profile-service ./backend/profile-service
                    docker build -t frontend ./frontend
                    '''
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY'
                }
            }
        }

        stage('Tag and Push Images to ECR') {
            steps {
                script {
                    sh '''
                    docker tag hello-service:latest $ECR_REGISTRY/hello-service:$IMAGE_TAG
                    docker push $ECR_REGISTRY/hello-service:$IMAGE_TAG

                    docker tag profile-service:latest $ECR_REGISTRY/profile-service:$IMAGE_TAG
                    docker push $ECR_REGISTRY/profile-service:$IMAGE_TAG

                    docker tag frontend:latest $ECR_REGISTRY/frontend-app:$IMAGE_TAG
                    docker push $ECR_REGISTRY/frontend-app:$IMAGE_TAG
                    '''
                }
            }
        }
    }
}
