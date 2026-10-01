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
        stage('Health Check') {
            steps {
                echo 'Starting application health check...'
                sh '''
                    docker rm -f health-check-test 2>/dev/null || true
                    docker run -d --name health-check-test -p 3010:3000 app-image-secure:latest
                    sleep 5
                    curl -f http://localhost:3010/
                    docker rm -f health-check-test
                '''
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

