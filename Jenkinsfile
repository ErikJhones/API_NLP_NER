def sendNotification() {
    googlechatnotification url: CHAT_ROOMS,
        message: "Task: Update and deliver ${APP_NAME} \nBranch: ${GIT_BRANCH} \nStatus: ${currentBuild.result} \nBuild Number: ${BUILD_NUMBER} \nBuild Link: ${BUILD_URL}"
}


pipeline {

    agent any

    options {
        skipDefaultCheckout true
    }

    environment {
        APP_NAME = 'thina-ia-api'
        GIT_URL = 'https://bitbucket.org/ead2pcdteam/sfp-ai-api.git'

        GIT_BRANCH = 'development'
        ENV_NAME = 'test'
        POETRY_VERSION = '1.1.7'
        IMAGE_ARGS = "--build-arg APP_NAME=${APP_NAME} --build-arg POETRY_VERSION=${POETRY_VERSION}"
        DEPLOYMENT_DIR = '/data/apps/thina-ia-api'

        // credentials
        GIT_CREDENTIAL = 'bitbucket-cloudteam'
        REGISTRY_ADDRESS = credentials('lead-main-ecr-url')
        REGISTRY_KEYS = 'ecr:us-east-1:lead-main-jenkins-ecr-keys'
        DEPLOYMENT_SSH_CREDENTIAL = 'ssh-jenkins'
        DEPLOYMENT_IP = credentials('projetosfp-ip')
        CHAT_ROOMS = 'id:webhook-system-notifications, id:webhook-sfp-jenkins'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: GIT_BRANCH,
                    credentialsId: GIT_CREDENTIAL,
                    url: GIT_URL
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.withRegistry('https://${REGISTRY_ADDRESS}', REGISTRY_KEYS) {
                        def customImage = docker.build('${APP_NAME}:${ENV_NAME}', '${IMAGE_ARGS} .')
                        customImage.push()
                    }
                }
                sh 'docker image rm ${APP_NAME}:${ENV_NAME} ${REGISTRY_ADDRESS}/${APP_NAME}:${ENV_NAME}'
            }
        }

        stage('Deploy') {
            steps {
                sshagent (credentials: [DEPLOYMENT_SSH_CREDENTIAL]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${DEPLOYMENT_IP} "cd ${DEPLOYMENT_DIR} \
                        && printf \'\\n\\n########## Update local image ##########\\n\\n\' \
                        && docker-compose down \
                        && docker image rm ${REGISTRY_ADDRESS}/${APP_NAME}:${ENV_NAME} \
                        && docker image pull ${REGISTRY_ADDRESS}/${APP_NAME}:${ENV_NAME}"

                        scp -o StrictHostKeyChecking=no docker-compose.yml jenkins@${DEPLOYMENT_IP}:${DEPLOYMENT_DIR}/

                        ssh -o StrictHostKeyChecking=no ${DEPLOYMENT_IP} "cd ${DEPLOYMENT_DIR} \
                        && printf \'\\n\\n########## Run container ##########\\n\\n\' \
                        && docker-compose up -d \
                        && docker-compose ps"
                    '''
                }
            }
        }
    }

    post {
         always {
            sh '''
                docker image prune -f
                docker images
            '''
        }

        failure {sendNotification()}

        success {
            sendNotification()

            dir("${WORKSPACE}@tmp") {
                deleteDir()
            }
            deleteDir()
        }
    }
}
