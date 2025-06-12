#!groovy
pipeline {
    agent any

    environment {
        registry = "docker-registry.wemove.com/diplanung-dcat-ap-eia"
        dockerImageName = script {
            def tag = determineTag(env.BRANCH_NAME, env.TAG_NAME)
            if (tag) {
                return registry + ":" + tag
            }
            return ""
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '5'))
        gitLabConnection('GitLab (wemove)')
    }

    stages {
        stage('Build Image') {
            when {
                expression { return env.dockerImageName != "" }
            }
            steps {
                script {
                    dockerImage = docker.build env.dockerImageName
                    echo "Docker image ${env.dockerImageName} built successfully."
                }
            }
        }
        stage('Push Image') {
            when {
                expression { return env.dockerImageName != "" }
            }
            steps {
                script {
                    dockerImage.push()
                    echo "Docker image ${env.dockerImageName} pushed successfully."
                }
            }
        }
    }

    post {
        changed {
            script {
                emailext (
                    body: '${DEFAULT_CONTENT}',
                    subject: '${DEFAULT_SUBJECT}',
                    to: '${DEFAULT_RECIPIENTS}',
                    recipientProviders: [developers(), requestor()]
                )
            }
        }
    }
}

def determineTag(branchName, tagName) {
    def tag = ""
    if (tagName) {
        tag = tagName
    } else if (branchName == 'develop') {
        tag = "latest"
    } else if (branchName && branchName.startsWith('feature/')) {
        def featureName = branchName.substring('feature/'.length())
        tag = "feature-${featureName}"
    }
    return tag
}
