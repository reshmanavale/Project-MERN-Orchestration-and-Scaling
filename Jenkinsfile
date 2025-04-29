pipeline {
    agent any

    environment {
        AWS_REGION = 'us-west-1'
        IMAGE_TAG = "${env.BUILD_NUMBER}"

        // ECR repository URIs (replace with your actual repo names if different)
        FRONTEND_ECR_URI = '975050024946.dkr.ecr.us-west-1.amazonaws.com/frontend-app'
        HELLO_SERVICE_ECR_URI = '975050024946.dkr.ecr.us-west-1.amazonaws.com/hello-service'
        PROFILE_SERVICE_ECR_URI = '975050024946.dkr.ecr.us-west-1.amazonaws.com/profile-service'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-creds', // ID of your stored Jenkins credentials
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    script {
                        sh """
                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${FRONTEND_ECR_URI}
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${HELLO_SERVICE_ECR_URI}
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${PROFILE_SERVICE_ECR_URI}
                        """
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh """
                    docker build -t frontend:${IMAGE_TAG} ./frontend
                    docker build -t hello-service:${IMAGE_TAG} ./backend/hello-service
                    docker build -t profile-service:${IMAGE_TAG} ./backend/profile-service
                    """
                }
            }
        }

        stage('Tag Docker Images for ECR') {
            steps {
                script {
                    sh """
                    docker tag frontend:${IMAGE_TAG} ${FRONTEND_ECR_URI}:${IMAGE_TAG}
                    docker tag hello-service:${IMAGE_TAG} ${HELLO_SERVICE_ECR_URI}:${IMAGE_TAG}
                    docker tag profile-service:${IMAGE_TAG} ${PROFILE_SERVICE_ECR_URI}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Push Docker Images to ECR') {
            steps {
                script {
                    sh """
                    docker push ${FRONTEND_ECR_URI}:${IMAGE_TAG}
                    docker push ${HELLO_SERVICE_ECR_URI}:${IMAGE_TAG}
                    docker push ${PROFILE_SERVICE_ECR_URI}:${IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up Docker environment"
            sh 'docker system prune -af'
        }
        success {
            echo "Docker images built and pushed to ECR successfully!"
        }
        failure {
            echo "Something went wrong during the build or push process."
        }
    }
}
