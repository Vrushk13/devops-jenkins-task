node {
agent any{

  stage('Build') {
        echo 'Building the application...'
        sh 'ls -la'
    }

    stage('Test') {
        echo 'Testing the application...'
        sh 'python3 --version'
    }

    stage('Docker Check') {
        echo 'Checking Docker...'
        sh 'docker --version'
        sh 'test -f Dockerfile'
    }

    stage('Finish') {
        echo 'Jenkins pipeline completed successfully!'
    }
}
