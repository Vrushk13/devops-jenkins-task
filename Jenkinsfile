```groovy
pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Building the application...'
                sh 'ls -la'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing the application...'
                sh 'python3 --version'
                sh 'python3 -m py_compile app.py'
            }
        }

        stage('Docker Check') {
            steps {
                echo 'Checking Docker...'
                sh 'docker --version'
                sh 'test -f Dockerfile'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t app-image-secure:latest .'
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Scanning Docker image with Trivy...'
                sh 'trivy image --scanners vuln --severity HIGH,CRITICAL app-image-secure:latest'
            }
        }

        stage('Finish') {
            steps {
                echo 'Jenkins pipeline completed successfully!'
            }
        }
    }
}

