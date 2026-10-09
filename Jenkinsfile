pipeline {
    agent any

    environment {
        IMAGE_NAME = "student-app"
        CONTAINER_NAME = "student-app-container"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run new container') {
            steps {
                withCredentials([string(credentialsId: 'db-password', variable: 'DB_PASSWORD')]) {
                    sh '''
                        docker rm -f $CONTAINER_NAME || true
                        docker run -d \
                            --name $CONTAINER_NAME \
                            -p 8000:8000 \
                            -e DB_PASSWORD \
                            $IMAGE_NAME
                    '''
                }
            }
        }
    }
}
