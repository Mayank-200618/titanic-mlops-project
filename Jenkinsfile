pipeline {
    agent any
    environment {
        DOCKER_HUB_ORGANIZATION = 'mayankmewara2006'
        CONTAINER_IMAGE_NAME    = 'titanic-mlops-project'
    }
    stages {
        stage('Sourcing Code') {
            steps {
                echo 'Syncing workspace...'
            }
        }
        stage('Pre-Flight Test') {
            steps {
                bat 'docker --version'
            }
        }
        stage('Docker Build') {
            steps {
                bat "docker build -t %DOCKER_HUB_ORGANIZATION%/%CONTAINER_IMAGE_NAME%:latest ."
            }
        }
        stage('Health Check') {
            steps {
                bat "docker run -d -p 5000:5000 --name pipeline_test %DOCKER_HUB_ORGANIZATION%/%CONTAINER_IMAGE_NAME%:latest"
                bat 'ping -n 8 127.0.0.1 > nul'
                bat 'curl -f http://localhost:5000/health'
            }
            post {
                always {
                    bat 'docker rm -f pipeline_test || exit /b 0'
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-vault-key', passwordVariable: 'HUB_PASSWORD', usernameVariable: 'HUB_USERNAME')]) {
                    bat 'echo %HUB_PASSWORD% | docker login -u %HUB_USERNAME% --password-stdin'
                    bat "docker push %DOCKER_HUB_ORGANIZATION%/%CONTAINER_IMAGE_NAME%:latest"
                }
            }
        }
    }
    post {
        always {
            bat 'docker logout || exit /b 0'
        }
    }
}