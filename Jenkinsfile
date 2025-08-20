pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        DATABASE_URL = 'sqlite:///:memory:'
        AUTH_TOKENS = 'test-token'
        FLASK_ENV = 'testing'
        PYTHONPATH = "${WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git --version'
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                echo "📦 Installing dependencies..."
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest pytest-html pytest-cov
                '''
            }
        }
        
        stage('Lint') {
            steps {
                sh '''
                echo "🔍 Running linting..."
                pip install pylint
                pylint app/ tests/ --exit-zero || true
                '''
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh '''
                        echo "🧪 Running unit tests..."
                        python -m pytest tests/ -v --junitxml=test-results/junit.xml
                        '''
                    }
                }
                
                stage('Integration Tests') {
                    steps {
                        sh '''
                        echo "🔗 Running integration tests..."
                        python -m pytest tests/ -v -m "integration" --junitxml=test-results/integration.xml
                        '''
                    }
                }
            }
        }
        
        stage('Coverage') {
            steps {
                sh '''
                echo "📊 Running coverage..."
                python -m pytest tests/ --cov=app --cov-report=xml --cov-report=html
                '''
            }
        }
        
        stage('Build Docker') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "🐳 Building Docker image..."
                    docker.build("pointr-api:${env.BUILD_ID}")
                }
            }
        }
    }
    
    post {
        always {
            echo "📦 Archiving artifacts..."
            archiveArtifacts artifacts: 'test-results/*.xml', fingerprint: true
            junit 'test-results/*.xml'
            
            script {
                if (fileExists('coverage.xml')) {
                    publishCobertura coverageCobertura: 'coverage.xml'
                }
                if (fileExists('htmlcov/index.html')) {
                    publishHTML target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ]
                }
            }
        }
        success {
            echo "✅ Pipeline succeeded!"
            slackSend color: 'good', message: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        failure {
            echo "❌ Pipeline failed!"
            slackSend color: 'danger', message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}