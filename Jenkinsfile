pipeline {
    agent any

    environment {
        TEST_IMAGE = 'electricity-predict-tests'
        ETL_IMAGE = 'electricity-predict-etl'
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_DEFAULT_REGION = 'eu-north-1' 
    }

    stages {
        
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Dreipfelt/Electricity-predict-Jenkins.git'
        stage('Build Test Container') {
            steps {
                sh 'docker build -t ${TEST_IMAGE} -f tests/Dockerfile .'
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                        --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
                        --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
                        --env AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
                        paycare-tests
            '''
            }
        }

        stage('Build ETL Container') {
            steps {
                sh 'docker build -t ${ETL_IMAGE} .'
            }
        }

        stage('Run ETL in Docker') {
            steps {
                script {
                    sh '''
                        docker run --rm \
                        -v ${WORKSPACE}/data:/app/data \
                        ${ETL_IMAGE}
                    '''

                    sh 'ls -l ${WORKSPACE}/data'
                }
            }
        }

    }

    post {
        success {
            echo '✅ ETL Pipeline completed successfully!'
            archiveArtifacts artifacts: 'data/output_data.csv', fingerprint: true
        }
        failure {
            echo '❌ ETL Pipeline failed.'
        }
    }
}
