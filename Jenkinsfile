pipeline {
    agent any

    environment {
        IMAGE_NAME = 'student-app'
        CONTAINER_NAME = 'student-app-container'
        APP_PORT = '8001'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t student-app .'
            }
        }

        stage('Deploy Application') {
            steps {
                withCredentials([string(credentialsId: 'db-password', variable: 'DB_PASSWORD')]) {
                    sh '''
                        docker rm -f student-app-container || true

                        docker run -d \
                            --name student-app-container \
                            -p 8001:8000 \
                            -e DB_PASSWORD \
                            student-app
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    sleep 5
                    docker ps --filter name=student-app-container
                    docker logs student-app-container --tail 20
                '''
            }
        }
    }

    post {
        success {
            echo 'Application deployment completed successfully.'
        }
        failure {
            echo 'Deployment failed. Check Console Output.'
        }
    }
}
