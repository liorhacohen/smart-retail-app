pipeline {
    agent {
        docker {
            image 'node:18'
            args '-u root:root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Python and Dependencies') {
            steps {
                sh '''
                    # Update package list
                    apt-get update
                    
                    # Install Python 3, pip, and venv
                    apt-get install -y python3 python3-pip python3-venv
                    
                    # Verify all installations
                    echo "=== Installed Versions ==="
                    node --version
                    npm --version
                    python3 --version
                    pip3 --version
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