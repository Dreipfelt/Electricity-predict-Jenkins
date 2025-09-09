CICD
Introduction to Jenkins 🧑‍💼
60 min
What you will learn in this course 🧐🧐

Jenkins is one of the most popular open-source continuous integration, delivery, and deployment servers designed to make collaborative software development easier. It is one of the earliest open-source continuous integration servers and remains the most common option in use today.

In this course, you will learn:

    What is Jenkins
    Install Jenkins using Docker compose
    How to setup basic and advanced pipelines in Jenkins
    Groovy Language basics

What is Jenkins

Over the years, Jenkins has evolved into a powerful and flexible system of automating software-related tasks. Jenkins itself serves mainly as an automation framework with much of the important logic implemented through a library of plugins. Everything from listening for web hooks or watching repositories to building environments and language support is handled by plugins, providing a great deal of flexibility.

Jenkins’ pipeline workflow —also provided through a plugin— is a relatively new addition, available as of 2016. The CI process can be defined either declaratively or imperatively using the Groovy language in files within the repository itself or through text boxes in the Jenkins web UI. One common criticism of Jenkins is that the plugin-centric configuration model and ability to define pipeline or build processes outside of repositories can sometimes make it difficult to easily replicate a configuration on a different Jenkins instance.

Jenkins is written in Java and released under an MIT license.
🛠️ Jenkins Installation Walkthrough (Local Setup using Docker)

FYI we're mostly following the installation tutorial found here
On macOS and Linux

    Open up a terminal window.

    Create a bridge network in Docker using the following docker network create command:

docker network create jenkins

    In order to execute Docker commands inside Jenkins nodes, download and run the docker:dind Docker image using the following docker run command:

docker run \
--name jenkins-docker \ #1
--rm \ #2
#--detach \ #3
--privileged \ #4
--network jenkins \ #5
--network-alias docker \ #6
--env DOCKER_TLS_CERTDIR=/certs \ #7
--volume jenkins-docker-certs:/certs/client \ #8
--volume jenkins-data:/var/jenkins_home \ #9
--publish 2376:2376 \ #10
docker:dind \ #11
--storage-driver overlay2 #12

    ( Optional ) Specifies the Docker container name to use for running the image. By default, Docker generates a unique name for the container.
    ( Optional ) Automatically removes the Docker container (the replica of the Docker image) when it is shut down.
    ( Optional ) Runs the Docker container in the background. You can stop this process by running docker stop jenkins-docker.
    Running Docker in Docker currently requires privileged access to function properly. This requirement may be relaxed with newer Linux kernel versions.
    This corresponds with the network created in the earlier step.
    Makes the Docker in Docker container available as the hostname docker within the jenkins network.
    Enables the use of TLS in the Docker server. Due to the use of a privileged container, this is recommended, though it requires the use of the shared volume described below. This environment variable controls the root directory where Docker TLS certificates are managed.
    Maps the /certs/client directory inside the container to a Docker volume named jenkins-docker-certs as created above.
    Maps the /var/jenkins_home directory inside the container to the Docker volume named jenkins-data. This allows for other Docker containers controlled by this Docker container’s Docker daemon to mount data from Jenkins.
    ( Optional ) Exposes the Docker daemon port on the host machine. This is useful for executing docker commands on the host machine to control this inner Docker daemon.
    The docker:dind image itself. Download this image before running, by using the command: docker image pull docker:dind.
    The storage driver for the Docker volume. Refer to the Docker storage drivers documentation for supported options.

If you have problems copying and pasting the above command snippet, use the annotation-free version below:

docker run --name jenkins-docker --rm \
  --privileged --network jenkins --network-alias docker \
  --env DOCKER_TLS_CERTDIR=/certs \
  --volume jenkins-docker-certs:/certs/client \
  --volume jenkins-data:/var/jenkins_home \
  --publish 2376:2376 \
  docker:dind --storage-driver overlay2

    Customize the official Jenkins Docker image, by executing the following two steps:
    Create a Dockerfile with the following content:

FROM jenkins/jenkins:2.504.2-jdk21
USER root
RUN apt-get update &amp;&amp; apt-get install -y lsb-release ca-certificates curl &amp;&amp; \
    install -m 0755 -d /etc/apt/keyrings &amp;&amp; \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc &amp;&amp; \
    chmod a+r /etc/apt/keyrings/docker.asc &amp;&amp; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
    https://download.docker.com/linux/debian $(. /etc/os-release &amp;&amp; echo \"$VERSION_CODENAME\") stable" \
    | tee /etc/apt/sources.list.d/docker.list &gt; /dev/null &amp;&amp; \
    apt-get update &amp;&amp; apt-get install -y docker-ce-cli &amp;&amp; \
    apt-get clean &amp;&amp; rm -rf /var/lib/apt/lists/*
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow json-path-api"

    Build a new docker image from this Dockerfile, and assign the image a meaningful name, such as "myjenkins-blueocean:2.504.2-1":

docker build -t myjenkins-blueocean:2.504.2-1 .

If you have not yet downloaded the official Jenkins Docker image, the above process automatically downloads it for you.

    Run your own myjenkins-blueocean:2.504.2-1 image as a container in Docker using the following docker run command:

docker run \
  --name jenkins-blueocean \ #1
  --restart=on-failure \ #2
#  --detach \ #3
  --network jenkins \ #4
  --env DOCKER_HOST=tcp://docker:2376 \ #5
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \ #6
  --publish 50000:50000 \ #7
  --volume jenkins-data:/var/jenkins_home \ #8
  --volume jenkins-docker-certs:/certs/client:ro \ #9
  myjenkins-blueocean:2.504.2-1 #10

    ( Optional ) Specifies the Docker container name for this instance of the Docker image.
    Always restart the container if it stops. If it is manually stopped, it is restarted only when Docker daemon restarts or the container itself is manually restarted.
    ( Optional ) Runs the current container in the background, known as "detached" mode, and outputs the container ID. If you do not specify this option, then the running Docker log for this container is displayed in the terminal window.
    Connects this container to the jenkins network previously defined. The Docker daemon is now available to this Jenkins container through the hostname docker.
    Specifies the environment variables used by docker, docker-compose, and other Docker tools to connect to the Docker daemon from the previous step.
    Maps, or publishes, port 8080 of the current container to port 8080 on the host machine. The first number represents the port on the host, while the last represents the container’s port. For example, to access Jenkins on your host machine through port 49000, enter -p 49000:8080 for this option.
    ( Optional ) Maps port 50000 of the current container to port 50000 on the host machine. This is only necessary if you have set up one or more inbound Jenkins agents on other machines, which in turn interact with your jenkins-blueocean container, known as the Jenkins "controller". Inbound Jenkins agents communicate with the Jenkins controller through TCP port 50000 by default. You can change this port number on your Jenkins controller through the Security page. For example, if you update the TCP port for inbound Jenkins agents of your Jenkins controller to 51000, you need to re-run Jenkins via the docker run …​ command. Specify the "publish" option as follows: the first value is the port number on the machine hosting the Jenkins controller, and the last value matches the changed value on the Jenkins controller, for example,--publish 52000:51000. Inbound Jenkins agents communicate with the Jenkins controller on that port (52000 in this example). Note that WebSocket agents do not need this configuration.
    Maps the /var/jenkins_home directory in the container to the Docker volume with the name jenkins-data. Instead of mapping the /var/jenkins_home directory to a Docker volume, you can also map this directory to one on your machine’s local file system. For example, specify the option --volume $HOME/jenkins:/var/jenkins_home to map the container’s /var/jenkins_home directory to the jenkins subdirectory within the $HOME directory on your local machine — typically /Users/<your-username>/jenkins or /home/<your-username>/jenkins. NOTE: If you change the source volume or directory for this, the volume from the docker:dind container above needs to be updated to match this.
    Maps the /certs/client directory to the previously created jenkins-docker-certs volume. The client TLS certificates required to connect to the Docker daemon are now available in the path specified by the DOCKER_CERT_PATH environment variable.
    The name of the Docker image, which you built in the previous step.

If you have problems copying and pasting the command snippet, use the annotation-free version below:

docker run --name jenkins-blueocean --restart=on-failure \
  --network jenkins --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  myjenkins-blueocean:2.504.2-1

    Proceed to the Post-installation setup wizard

On Windows

The Jenkins project provides a Linux container image, not a Windows container image. Be sure that your Docker for Windows installation is configured to run Linux Containers rather than Windows Containers. Refer to the Docker documentation for instructions to switch to Linux containers. Once configured to run Linux Containers, the steps are:

    Open up a command prompt window and similar to the macOS and Linux instructions above do the following:

    Create a bridge network in Docker

docker network create jenkins

    Run a docker:dind Docker image

docker run --name jenkins-docker --rm ^
  --privileged --network jenkins --network-alias docker ^
  --env DOCKER_TLS_CERTDIR=/certs ^
  --volume jenkins-docker-certs:/certs/client ^
  --volume jenkins-data:/var/jenkins_home ^
  --publish 2376:2376 ^
  docker:dind

    Customize the official Jenkins Docker image, by executing the following two steps:

Create a Dockerfile with the following content:

FROM jenkins/jenkins:2.504.2-jdk21
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow json-path-api"

Build a new docker image from this Dockerfile and assign the image a meaningful name, e.g. "myjenkins-blueocean:2.504.2-1":

docker build -t myjenkins-blueocean:2.504.2-1 .

If you have not yet downloaded the official Jenkins Docker image, the above process automatically downloads it for you.

    Run your own myjenkins-blueocean:2.504.2-1 image as a container in Docker using the following docker run command:

docker run --name jenkins-blueocean --restart=on-failure ^
  --network jenkins --env DOCKER_HOST=tcp://docker:2376 ^
  --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 ^
  --volume jenkins-data:/var/jenkins_home ^
  --volume jenkins-docker-certs:/certs/client:ro ^
  --publish 8080:8080 --publish 50000:50000 myjenkins-blueocean:2.504.2-1

    Proceed to the Setup wizard.

Post-installation setup wizard

After downloading, installing and running Jenkins using one of the procedures above (except for installation with Jenkins Operator), the post-installation setup wizard begins.

This setup wizard takes you through a few quick "one-off" steps to unlock Jenkins, customize it with plugins and create the first administrator user through which you can continue accessing Jenkins.
Unlocking Jenkins

When you first access a new Jenkins controller, you are asked to unlock it using an automatically-generated password.

    Browse to http://localhost:8080 (or whichever port you configured for Jenkins when installing it) and wait until the Unlock Jenkins page appears.

Unlock Jenkins page

    From the Jenkins console log output, copy the automatically-generated alphanumeric password (between the 2 sets of asterisks).

Copying initial admin password
Note:

    The command: sudo cat /var/lib/jenkins/secrets/initialAdminPassword will print the password at console.

    If you are running Jenkins in Docker using the official jenkins/jenkins image you can use sudo docker exec ${CONTAINER_ID or CONTAINER_NAME} cat /var/jenkins_home/secrets/initialAdminPassword to print the password in the console without having to exec into the container.

    On the Unlock Jenkins page, paste this password into the Administrator password field and click Continue.

Customizing Jenkins with plugins

After unlocking Jenkins, the Customize Jenkins page appears. Here you can install any number of useful plugins as part of your initial setup.

Click one of the two options shown:

    Install suggested plugins - to install the recommended set of plugins, which are based on most common use cases.

    Select plugins to install - to choose which set of plugins to initially install. When you first access the plugin selection page, the suggested plugins are selected by default.

TIP

If you are not sure what plugins you need, choose Install suggested plugins. You can install (or remove) additional Jenkins plugins at a later point in time via the Manage Jenkins > Plugins page in Jenkins.

The setup wizard shows the progression of Jenkins being configured and your chosen set of Jenkins plugins being installed. This process may take a few minutes.
Creating the first administrator user

Finally, after customizing Jenkins with plugins, Jenkins asks you to create your first administrator user.

    When the Create First Admin User page appears, specify the details for your administrator user in the respective fields and click Save and Finish.

    When the Jenkins is ready page appears, click Start using Jenkins.
    Notes:

        This page may indicate Jenkins is almost ready! instead and if so, click Restart.

        If the page does not automatically refresh after a minute, use your web browser to refresh the page manually.

    If required, log in to Jenkins with the credentials of the user you just created and you are ready to start using Jenkins!

✅ If you see the dashboard, your Jenkins installation is complete!
🚀 Jenkins Walkthrough: Create Your First Job (Freestyle Project)
🎯 Goal:

Set up and run a simple Jenkins job that prints “Hello World” using a Freestyle Project.
✅ Step 1: Navigate to Jenkins Dashboard

    Open your web browser and go to your local Jenkins instance:

    http://localhost:8080

    Log in if needed.

✅ Step 2: Create a New Job

    On the Jenkins dashboard, click “New Item” (or “Create a Job”).

    Enter a job name, for example:

    my-first-job

    Select Freestyle Project.

    Click OK.

✅ Step 3: Configure the Job
🔷 General Section:

    Add a description (optional), e.g.:

    This is my first Jenkins Freestyle job.

🔷 Source Code Management:

    Leave it set to None (unless using GitHub or other repositories).

🔷 Build Triggers (Optional, skip for now):

    These define when Jenkins should run the job.

    Options include:
        Remote trigger
        Build after other projects
        Cron schedule (periodic build)
        GitHub hook trigger
        Poll SCM (monitor Git repo for changes)

    ✅ For now: Do not select any triggers.

🔷 Build Environment:

    This section can be used to:
        Clean the workspace before builds
        Add environment variables
        Add timestamps
        Use secrets (advanced)

    ✅ For now: Leave defaults.

✅ Step 4: Define the Build Step

    Scroll to the Build section.

    Click “Add build step” → “Execute shell”.

    Enter the following command:

    echo "Hello World"

    Click Apply to save changes.

✅ Step 5: (Optional) Post-Build Actions

    Leave this section empty for now.

    Post-build actions can include:
        Email or Slack notifications
        HTML reports
        Cleaning up workspace after build

✅ Step 6: Save and Run the Job

    Click Save.
    On the job’s main page, click “Build Now”.

✅ Step 7: Check Console Output

    Click on the build number (e.g., #1) in the Build History.

    Click “Console Output”.

    Verify that the output includes:

    Hello World

    You’ll also see build logs and the shell command executed.

🎉 Done!

You’ve successfully created and executed your first Jenkins Freestyle job.
🧪 Jenkins Walkthrough: Automate a Real-World Web Scraper with Freestyle Job
🎯 Goal:

Create a Jenkins Freestyle job that clones a web scraper project from GitHub, builds a Docker image, runs it, and sets up automatic builds on repository changes.
✅ Step 1: Locate the Sample Web Scraper Repo

    Go to Jedha Bootcamp’s GitHub account.

    Find the repo named sample-web-scrapper.

    This project:
        Scrapes Jedha's latest blog posts.
        Includes a Dockerfile and requirements.txt for setup.

✅ Step 2: Create a New Freestyle Job

    Go to Jenkins Dashboard.

    Click “New Item”.

    Name the job:

    scrapper

    Select Freestyle project, then click OK.

✅ Step 3: General Configuration

    Add a description:

    Scrape Jedha's latest blog posts.

✅ Step 4: Set Up Source Code Management

    Select Git.

    Paste the GitHub repository URL.

    Remove any tree/main or blob/main fragments from the URL.

    Specify the branch:

    main

    (Optional) If private repo:
        Add GitHub credentials (via Add → Jenkins).
        Use your GitHub Personal Access Token.

✅ Step 5: Configure Build Triggers

To automatically build on code updates:

    Check Poll SCM.

    Enter the cron schedule:

    H/5 * * * *

    This polls the repo every 5 minutes.

✅ Step 6: Add Build Steps
Step 6.1: Build Docker Image

    Click Add build step → Execute shell.

    Add:

    docker build -t simple-web-scrapper .

Step 6.2: Run Docker Container

    Add another Execute shell step.

    Add:

    docker run simple-web-scrapper

✅ Step 7: Post-Build Actions (Optional)

    Add a notification or email alert if build fails.
    Example: Send yourself an email on failure.

✅ Step 8: Save and Run the Job

    Click Save.
    Click Build Now to run it manually.

✅ Step 9: Inspect the Console Output

    Click the build number (e.g., #1) in the Build History.

    Select Console Output.

    Look for:
        Docker build logs
        Confirmation of articles scraped (e.g., "3 logged articles")

✅ Step 10: Verify the Scraper Output

Check the code in scrapper.py:

    Functions:
        fetch_latest_post()
        log_post()

    Confirms it logs how many articles were scraped.

🎉 Success! You’ve built and automated a real web scraping pipeline in Jenkins!
🚀 Jenkins Walkthrough: Creating a Custom Pipeline with Groovy and Jenkinsfile
IMPORTANT
|
If you follow along, you will have a error

If it's the first time you watch the video below, you will have an error in your pipeline when I have everything running correctly and that is normal. I haven't showed you how to set up email notifications just yet (it's in the next video), feel free to skip the email notification part entirely for now as you'd need to set up an email server first. It's purposefully done so as I want you to understand Jenkinsfile and Groovy language first.

Email notification setup is fairly simple then 😊

Here is a structured step-by-step walkthrough for students to follow when creating a custom Jenkins pipeline using a Jenkinsfile written in Groovy, based on the transcript you provided.
🎯 Goal:

Set up a multi-stage Jenkins pipeline from a GitHub repo using a Jenkinsfile with Groovy syntax. Include build, test, (and optionally email notification) steps.
✅ Step 1: Understand the Setup

This pipeline:

    Clones the development branch of a repo.
    Builds a Docker image.
    Runs Python tests.
    Sends email notifications on success or failure.

It uses a Jenkinsfile in the repo’s root, written in Groovy, to define all pipeline logic.

Here's the fully commented jenkinsfile:

// The entire pipeline block defines the Jenkins pipeline
pipeline {

    // 'agent any' means the pipeline can run on any available Jenkins agent (machine)
    agent any

    // The 'stages' block contains all the steps of the CI pipeline
    stages {

        // === Stage 1: Clone the GitHub repository ===
        stage('Clone repository') {
            steps {
                // This clones the Git repo from the 'development' branch
                git branch: 'development', url: 'https://github.com/JedhaBootcamp/sample-web-scraper.git'
            }
        }

        // === Stage 2: Build a Docker image ===
        stage('Build Docker Image') {
            steps {
                script {
                    // This builds a Docker image from the Dockerfile in the repo
                    // The image will be tagged as 'simple-scraper:latest'
                    docker.build('simple-scraper:latest')
                }
            }
        }

        // === Stage 3: Run tests inside the Docker container ===
        stage('Run Tests') {
            steps {
                script {
                    // Run a command inside the Docker container built earlier
                    // This uses pytest to run tests and outputs results to results.xml
                    docker.image('simple-scraper:latest').inside {
                        sh 'pytest tests/tests.py --junitxml=results.xml'
                    }
                }
            }
        }

        // === Stage 4: Archive test results ===
        stage('Archive Results') {
            steps {
                // This tells Jenkins to store the test result file so it can be displayed in the UI
                junit 'results.xml'
            }
        }
    }

    // === Post actions (run after the pipeline finishes) ===
    post {
        // If the pipeline is successful
        success {
            script {
                echo "Success" // Log message in Jenkins console

                // Send an email notification about the successful build
                emailext(
                    subject: "Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """<p>Good news!</p>
                             <p>The build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> was successful.</p>
                             <p>View the details <a href="${env.BUILD_URL}">here</a>.</p>""",
                    to: 'antoine@jedha.co'
                )
            }
        }

        // If the pipeline fails
        failure {
            script {
                echo "Failure" // Log message in Jenkins console

                // Send an email notification about the failed build
                emailext(
                    subject: "Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """<p>Unfortunately, the build <b>${env.JOB_NAME} #${env.BUILD_NUMBER}</b> has failed.</p>
                             <p>Please check the logs and address the issues.</p>
                             <p>View the details <a href="${env.BUILD_URL}">here</a>.</p>""",
                    to: 'antoine@jedha.co'
                )
            }
        }
    }
}

✅ Step 2: Check Out the Development Branch Locally (Optional)

If cloning locally, switch to the development branch:

git checkout -b development
git pull origin development

✅ Step 3: Understand the Jenkinsfile Stages

The Jenkinsfile contains:

    pipeline declaration

    agent any: use any available agent

    stages:
        Clone repo (development branch)
        Build Docker image: docker.build("simple-scrapper")
        Run tests using pytest and save results to results.xml
        Publish test results

    post section:
        On success: Send success email
        On failure: Send failure email

✅ Step 4: Create a New Jenkins Pipeline Job

    Go to Jenkins dashboard → New Item.

    Name:

    my-first-pipeline

    Select Pipeline, then click OK.

✅ Step 5: Configure the Pipeline Job
🔷 General

    Description:

    Custom pipeline using Groovy language

🔷 Build Triggers

Enable automatic build:

    Check Poll SCM
    Cron schedule:

H/5 * * * *

🔷 Pipeline Configuration

    In the Pipeline section, choose:
        Definition: Pipeline script from SCM
        SCM: Git

    Paste your GitHub repository URL: https://github.com/JedhaBootcamp/sample-web-scraper.

    Branch:

    development

Script Path:

Jenkinsfile

    (Only change this if your Jenkinsfile is in a subdirectory.)

✅ Step 6: Save and Run the Pipeline

    Click Save.
    On the job page, click Build Now.

✅ Step 7: Inspect the Build Output

    Click the build number under Build History.

    Click Console Output to watch the stages:
        Clone
        Build Docker image
        Run tests
        Publish results
        Send email based on result

✅ If the tests pass, a success email is sent. ❌ If the tests fail, a failure email is sent.
✅ Step 8: Test the Failure Path (Optional)

    Modify the test in the test.py file to cause a failure.

    Push changes:

    git add .
    git commit -m "force failure"
    git push origin development

    Jenkins will detect the change and rerun the pipeline.

📝 You should see:

    A failed test in the output.
    A failure notification email.

🧠 Notes on Jenkinsfile and Groovy

    The Jenkinsfile is written in Groovy, a declarative scripting language.
    You don’t need to master Groovy, but understanding syntax like pipeline, stage, steps, and post is key to customizing pipelines.

🎉 Well done! You now know how to use a Jenkinsfile to define complex pipelines with testing, branching, and notification capabilities.
📧 Jenkins Email Notifications Setup Using Postmark (Optional)
Jenkins Email Notification Walkthrough

Jenkins Email Notification Walkthrough

Jenkins Email Notification Walkthrough

Jenkins Email Notification Walkthrough

🧰 Jenkins Console Walkthrough: Accessing Build Artifacts via Docker (OPTIONAL)
View Jenkins console walkthrough

View Jenkins console walkthrough

View Jenkins console walkthrough

View Jenkins console walkthrough

View Jenkins console walkthrough

View Jenkins console walkthrough

View Jenkins console walkthrough

View Jenkins console walkthrough

View Jenkins console walkthrough

View Jenkins console walkthrough

Resources 📚📚

    Intro to Jenkins
    Jenkins Pipeline
    How to Configure Email Notification in Jenkins Pipeline Using the Mailer Plugin
    Postmarkapp Documentation
