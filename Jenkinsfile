pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Available Tools') {
            steps {
                sh '''
                    echo "Checking available tools..."
                    which node || echo "Node.js not found"
                    which npm || echo "npm not found"
                    which python3 || echo "Python3 not found"
                    which pip3 || echo "pip3 not found"
                '''
            }
        }

        stage('Backend: Install & Lint') {
            steps {
                dir('backend') {
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install --upgrade pip'
                    sh '. venv/bin/activate && pip install -r requirements.txt flake8 black isort'
                    sh '. venv/bin/activate && flake8 .'
                    sh '. venv/bin/activate && black --check .'
                    sh '. venv/bin/activate && isort --check-only .'
                }
            }
        }

        stage('Backend: Test') {
            steps {
                dir('backend') {
                    sh '. venv/bin/activate && pip install pytest pytest-cov'
                    sh '. venv/bin/activate && pytest --maxfail=1 --disable-warnings'
                }
            }
        }

        stage('Frontend: Install & Lint') {
            steps {
                dir('frontend') {
                    sh 'npm ci'
                    sh 'npm run lint'
                }
            }
        }

        stage('Frontend: Test') {
            steps {
                dir('frontend') {
                    sh 'npm test -- --watchAll=false'
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}