pipeline {
agent any

  stages {
      stage("Build image") {
          steps {
              script {
                docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                customImage = docker.build("facilittecnologia/superset:${env.BUILD_ID}")
                customImage.push()
              }
            }
        }
    }
}
}
