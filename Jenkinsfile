pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO = "865487342006.dkr.ecr.us-east-1.amazonaws.com/cicd"
        IMAGE_TAG = "${BUILD_NUMBER}"
        TERRAFORM_DIR = "terraform"
        BRANCH_NAME="main"
        }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/kambalaashok4/ci-cd-django-jenkins.git'

            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install coverage
                '''
            }
        }

        stage('Run Django Checks') {
            steps {
                sh 'python3 manage.py check'
            }
        }

        stage('Run Tests with Coverage') {
            steps {
                sh '''
                coverage run manage.py test
                coverage xml
                '''
            }
        }

        // ===============================
        // 🔥 NEW STAGE - SONARQUBE
        // ===============================

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    /opt/sonar-scanner/bin/sonar-scanner \
                    -Dsonar.projectKey=django-app \
                    -Dsonar.sources=. \
                    -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ===============================
        // Docker + ECR (unchanged)
        // ===============================

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t cicd:${IMAGE_TAG} .
                docker tag cicd:${IMAGE_TAG} ${ECR_REPO}:${IMAGE_TAG}
                """
            }
        }

        stage('Login to AWS ECR') {
            steps {
                sh """
                aws ecr get-login-password --region ${AWS_REGION} \
                | docker login --username AWS --password-stdin ${ECR_REPO}
                """
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                sh "docker push ${ECR_REPO}:${IMAGE_TAG}"
            }
        }

        stage('Trigger Deployment') {
            when {
                 expression { env.BRANCH_NAME == 'main' }
            }
            steps {
                sh """
                cd ${TERRAFORM_DIR}
                terraform init
                terraform plan -var="image_tag=${IMAGE_TAG}"
                terraform apply -auto-approve -var="image_tag=${IMAGE_TAG}"
                """
            }
        }
    }

    post {
        always {
            sh """
            docker rmi cicd:${IMAGE_TAG} ${ECR_REPO}:${IMAGE_TAG} || true
            docker system prune -af || true
            """
        }
    }
}