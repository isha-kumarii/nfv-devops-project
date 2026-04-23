pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/isha-kumarii/nfv-devops-project.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

    }
}
