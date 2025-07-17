# Smart Retail App Jenkins CI/CD Pipeline Setup Guide

This guide explains every step of the CI/CD pipeline for the Smart Retail App, using Jenkins for automation from initial setup to production deployment.

## 🎯 Pipeline Overview

The Jenkins CI/CD pipeline consists of 9 stages that ensure code quality, testing, security, and reliable deployment:

1. **Lint and Format Code** - Code quality checks
2. **Unit Testing** - Automated testing
3. **Build and Push Docker Images** - Containerization
4. **Deploy to Kubernetes** - Infrastructure deployment
5. **API Testing on Live Deployment** - Integration testing
6. **Monitoring Verification** - Observability setup
7. **Performance Testing** - Load testing (optional)
8. **Security Scanning** - Vulnerability assessment
9. **Notifications** - Status reporting

---

## 📋 Prerequisites

Before setting up the Jenkins CI/CD pipeline, ensure you have:

### 1. Jenkins Server
- Jenkins installed locally (see below) or on a remote server
- Access to Jenkins UI
- Jenkins plugins: Docker, Kubernetes CLI, Blue Ocean (optional), Credentials Binding

### 2. Docker Hub Account
- Docker Hub account for storing images
- Username and access token

### 3. Kubernetes Cluster
- Minikube (local development) or EKS (production)
- kubectl configured
- Cluster access credentials

### 4. Jenkins Credentials
Set up these credentials in Jenkins (Manage Jenkins → Credentials):
- **Docker Hub**: Username and password/token
- **Kubernetes Config**: Kubeconfig as a secret file or string
- **Slack Webhook** (optional): For notifications

---

## 🚀 Running Jenkins Locally (Optional)

You can run Jenkins locally using Docker:

```bash
docker build -t smart-retail-jenkins -f Dockerfile.jenkins .
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins smart-retail-jenkins
```

Access Jenkins at [http://localhost:8080](http://localhost:8080) and unlock it using the initial admin password (see container logs).

---

## 🛠️ Jenkins Pipeline Stages

The pipeline is defined in the root-level `Jenkinsfile` and includes the following stages:

1. **Lint and Format Code**
   - Python: flake8, black, isort
   - JavaScript: ESLint
2. **Unit Testing**
   - Backend: pytest
   - Frontend: npm test
3. **Build and Push Docker Images**
   - Backend and frontend images
   - Push to Docker Hub
4. **Deploy to Kubernetes**
   - Apply manifests using kubectl
5. **API Testing on Live Deployment**
   - Run integration tests
6. **Monitoring Verification**
   - Check Prometheus and Grafana
7. **Performance Testing** (optional)
   - Locust load tests
8. **Security Scanning**
   - Trivy for Docker images
9. **Notifications**
   - Slack or email (optional)

---

## 🔑 Jenkins Credentials Setup

1. Go to **Manage Jenkins → Credentials**
2. Add the following credentials:
   - **docker-hub-credentials**: Username/Password for Docker Hub
   - **kubeconfig**: Secret file or string for Kubernetes config
   - **slack-webhook** (optional): Secret text for Slack notifications

Reference these credentials in your `Jenkinsfile` using the `credentials()` helper or environment variables.

---

## 📝 Example Jenkinsfile Snippet

```groovy
pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig')
    }
    stages {
        stage('Lint and Format') {
            steps {
                sh 'cd backend && flake8 . && black . && isort .'
                sh 'cd frontend && npm run lint'
            }
        }
        // ... other stages ...
    }
}
```

---

## 🏗️ Pipeline Triggers

- **Push to main/develop branch**: Configure Jenkins to poll SCM or use webhooks
- **Manual trigger**: Start pipeline from Jenkins UI

---

## 🧪 Testing the Pipeline

1. Push code to your repository
2. Jenkins will detect changes and start the pipeline
3. Monitor progress in the Jenkins UI
4. Review logs and results for each stage

---

## 🛠️ Troubleshooting Jenkins Pipeline

- **Docker Build Fails**: Check Dockerfile syntax and context
- **Kubernetes Deploy Fails**: Verify kubeconfig and cluster access
- **Credential Errors**: Ensure credentials are set up in Jenkins
- **Test Failures**: Review logs for details

---

## 📚 Further Reading
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Credentials](https://www.jenkins.io/doc/book/using/using-credentials/)

---

**Your Jenkins pipeline is now ready to automate testing, building, and deployment for the Smart Retail App!** 