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
                sh '''
                    # Install git in the container
                    apt-get update
                    apt-get install -y git
                    
                    # Clean the workspace completely
                    rm -rf * .git .* 2>/dev/null || true
                    
                    # Clone the repository
                    git clone https://github.com/liorhacohen/smart-retail-app .
                    
                    echo "=== Repository cloned successfully ==="
                    ls -la
                '''
            }
        }

        stage('Install Python venv (if needed)') {
            steps {
                sh 'apt-get update && apt-get install -y python3-venv'
            }
        }

        stage('Install Python and Dependencies') {
            steps {
                sh '''
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
                    // Install dependencies globally for CI
                    sh 'pip3 install --upgrade pip'
                    sh 'pip3 install -r requirements.txt flake8 black isort'
                    sh 'flake8 .'
                    sh 'black --check .'
                    sh 'isort --check-only .'
                }
            }
        }

        stage('Backend: Test') {
            steps {
                dir('backend') {
                    sh 'pip3 install pytest pytest-cov'
                    sh 'pytest --maxfail=1 --disable-warnings'
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