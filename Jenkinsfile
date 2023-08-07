#!groovy

pipeline {
	agent none
    stage('Docker Build Image') {
    	agent any
      steps {
      	sh 'docker build -t keithkwok1904/webapp:latest .'
      }
    }
    stage('Docker Push Image to DockerHub') {
    	agent any
      steps {
      	withCredentials([usernamePassword(credentialsId: 'DockerHub', passwordVariable: 'DockerHubPassword', usernameVariable: 'DockerHubUser')]) {
        	sh "docker login -u ${env.DockerHubUser} -p ${env.DockerHubPassword}"
          sh 'docker push keithkwok1904/webapp:latest'
        }
      }
    }
  }
}
