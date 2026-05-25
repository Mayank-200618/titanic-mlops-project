pipeline {
    agent any
    environment {
        DOCKER_HUB_ORGANIZATION = 'mayankmewara2006'
        CONTAINER_IMAGE_NAME    = 'titanic-mlops-project'
    }
    stages {
        stage('Sourcing Code') {
            steps {
                echo 'Syncing workspace from GitHub...'
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
                // Pauses execution for ~7 seconds allowing the Flask app inside the container to spin up fully
                bat 'ping -n 8 127.0.0.1 > nul'
                bat 'curl -f http://localhost:5000/health'
            }
            post {
                always {
                    // Forcefully stops and removes the integration test container even if curl fails
                    bat 'docker rm -f pipeline_test || exit /b 0'
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-vault-key', passwordVariable: 'HUB_PASSWORD', usernameVariable: 'HUB_USERNAME')]) {
                    // Safe execution parameters preventing Windows cmd space padding bugs
                    bat "docker login -u %HUB_USERNAME% -p %HUB_PASSWORD%"
                    
                    // Uses dynamic environment variables to match the image built in Stage 3
                    bat "docker push %DOCKER_HUB_ORGANIZATION%/%CONTAINER_IMAGE_NAME%:latest"
                }
            }
        } // Correctly closes the Push to Docker Hub stage
    } // Correctly closes the collective stages block
    post {
        always {
            // Wipes the local registry login tokens from the Windows server after completing execution loops
            bat 'docker logout || exit /b 0'
        }
    }
}