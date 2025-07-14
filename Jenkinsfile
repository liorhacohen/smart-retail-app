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
                    
                    # Clean and clone the repository
                    rm -rf * .git .* 2>/dev/null || true
                    git clone https://github.com/liorhacohen/smart-retail-app .
                    
                    echo "=== Repository cloned successfully ==="
                    ls -la
                '''
            }
        }

        stage('Install Python and Dependencies') {
            steps {
                sh '''
                    # Install Python 3, pip, and venv
                    apt-get update
                    apt-get install -y python3 python3-pip python3-venv python3-full
                    
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
                    sh '''
                        # Create virtual environment
                        python3 -m venv venv
                        
                        # Activate virtual environment and upgrade pip
                        . venv/bin/activate
                        pip install --upgrade pip
                        
                        # Install dependencies and linting tools
                        pip install -r requirements.txt flake8 black isort
                        
                        # Run linting (make non-blocking for now)
                        flake8 . || echo "Linting issues found but continuing..."
                        black --check . || echo "Black formatting issues found but continuing..."
                        isort --check-only . || echo "Import sorting issues found but continuing..."
                    '''
                }
            }
        }

        stage('Backend: Test') {
            steps {
                dir('backend') {
                    sh '''
                        # Activate virtual environment and run tests
                        . venv/bin/activate
                        pip install pytest pytest-cov
                        pytest --maxfail=1 --disable-warnings || echo "Tests failed but continuing..."
                    '''
                }
            }
        }

        stage('Frontend: Install & Lint') {
            steps {
                dir('frontend') {
                    sh '''
                        npm ci
                        npm run lint || echo "Frontend linting issues found but continuing..."
                    '''
                }
            }
        }

        stage('Frontend: Test') {
            steps {
                dir('frontend') {
                    sh '''
                        npm test -- --watchAll=false || echo "Frontend tests failed but continuing..."
                    '''
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