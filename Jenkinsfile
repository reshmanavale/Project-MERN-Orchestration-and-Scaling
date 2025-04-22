pipeline {
    agent any

    environment {
        AWS_REGION = 'us-west-1'
        ECR_FRONTEND_REPO = '975050024946.dkr.ecr.us-west-1.amazonaws.com/frontend-app'
        ECR_HELLO_REPO = '975050024946.dkr.ecr.us-west-1.amazonaws.com/hello-service'
        ECR_PROFILE_REPO = '975050024946.dkr.ecr.us-west-1.amazonaws.com/profile-service'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/reshmanavale/Project-MERN-Orchestration-and-Scaling.git'
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh '''
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin 975050024946.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh '''
                        docker build -t $ECR_FRONTEND_REPO:latest ./frontend
                        docker build -t $ECR_HELLO_REPO:latest ./backend/hello-service
                        docker build -t $ECR_PROFILE_REPO:latest ./backend/profile-service
                    '''
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh '''
                        docker push $ECR_FRONTEND_REPO:latest
                        docker push $ECR_HELLO_REPO:latest
                        docker push $ECR_PROFILE_REPO:latest
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
    }
}
