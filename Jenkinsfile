pipeline {
agent any

environment {
    REGISTRY_CREDENTIALS = 'docker-hub-credentials'
    IMAGE_NAME = 'mypractice/node-app'
    IMAGE_TAG = "${BUILD_NUMBER}"
}

stages {
    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Install Dependencies') {
        steps {
            sh 'npm ci'
        }
    }

    stage('Run Tests') {
        steps {
            sh 'npm test'
        }
    }

    stage('Build App') {
        steps {
            sh 'npm run build'
        }
    }

    stage('Build Docker Image') {
        steps {
            sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
        }
    }

    stage('Push Docker Image') {
        steps {
            script {
                docker.withRegistry('', REGISTRY_CREDENTIALS) {
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
}

post {
    always {
        cleanWs()
    }
    failure {
        echo 'Pipeline failed. Check the logs above.'
    }
}


}