pipeline {

    agent {
        dockerfile {
            filename 'Dockerfile'
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    environment {
        AWS_REGION    = "us-east-1"
        ECR_REPO      = "865487342006.dkr.ecr.us-east-1.amazonaws.com/cicd"
        IMAGE_TAG     = "${BUILD_NUMBER}"
        TERRAFORM_DIR = "terraform"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                pip install coverage
                '''
            }
        }

        stage('Run Django Checks') {
            steps {
                sh 'python manage.py check'
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

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    sonar-scanner \
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

        stage('Terraform Deploy (Main Only)') {
            when {
                branch 'main'
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
        success {
            echo "Pipeline completed successfully 🚀"
        }
        failure {
            echo "Pipeline failed ❌ Check logs above."
        }
    }
}