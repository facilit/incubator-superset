node {
   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      git branch: 'paraiba', credentialsId: 'ac4c8028-d6bf-40ba-8c2d-7e72de2d809b', url: 'https://github.com/facilit/incubator-superset.git'
   }
    stage('Build') {  
      def customImage = docker.build("facilittecnologia/superset:paraiba")
      customImage.push()
   }
}  
