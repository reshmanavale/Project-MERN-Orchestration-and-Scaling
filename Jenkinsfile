pipeline {
    agent any

    environment {
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/reshmanavale/Project-MERN-Orchestration-and-Scaling.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    dir('backend/hello-service') {
                        sh 'docker build -t hello-service:${IMAGE_TAG} .'
                    }
                    dir('backend/profile-service') {
                        sh 'docker build -t profile-service:${IMAGE_TAG} .'
                    }
                    dir('frontend') {
                        sh 'docker build -t frontend:${IMAGE_TAG} .'
                    }
                }
            }
        }

        stage('(Optional) Push to ECR') {
            when {
                expression { return false } // Skipping for now
            }
            steps {
                echo "Push to ECR skipped due to AWS credentials issue."
            }
        }
    }
}
