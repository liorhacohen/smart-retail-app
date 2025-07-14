pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.11'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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
                    // Install Node.js using NodeSource setup script
                    sh '''
                        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
                        sudo apt-get install -y nodejs
                    '''
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