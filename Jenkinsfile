pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = 'AKIA6GBMCU7ZIS77CDYD'
        AWS_SECRET_ACCESS_KEY = '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'
        AWS_REGION            = 'us-west-1'
        ECR_REGISTRY          = '975050024946.dkr.ecr.us-west-1.amazonaws.com'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/reshmanavale/Project-MERN-Orchestration-and-Scaling.git', branch: 'main'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                sh '''
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set region $AWS_REGION

                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $ECR_REGISTRY
                '''
            }
        }

        stage('Build and Push hello-service') {
            steps {
                dir('backend/helloService') {
                    sh '''
                        docker build -t hello-service .
                        docker tag hello-service:latest $ECR_REGISTRY/hello-service:latest
                        docker push $ECR_REGISTRY/hello-service:latest
                    '''
                }
            }
        }

        stage('Build and Push profile-service') {
            steps {
                dir('backend/profileService') {
                    sh '''
                        docker build -t profile-service .
                        docker tag profile-service:latest $ECR_REGISTRY/profile-service:latest
                        docker push $ECR_REGISTRY/profile-service:latest
                    '''
                }
            }
        }

        stage('Build and Push frontend') {
            steps {
                dir('frontend') {
                    sh '''
                        docker build -t frontend-app .
                        docker tag frontend-app:latest $ECR_REGISTRY/frontend-app:latest
                        docker push $ECR_REGISTRY/frontend-app:latest
                    '''
                }
            }
        }
    }
}
