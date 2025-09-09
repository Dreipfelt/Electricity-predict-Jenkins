Continuous Training
Airflow Server 🌬️
60 min
What you will learn in this course 🧐🧐

Final building block of this project: Airflow. The whole project needs to be orchastrated using this tool as you have a lot of independent moving pieces that needs to be organized. Airflow is one the most perfect candidate for that kind of tasks. In this course we will teach you:

    How to stage Airflow to production on HuggingFace Spaces
    A basic DAG that will manage Jenkins, MLflow and EC2

Demo setup

Here are useful links if you want to follow along with the demo below:

    Sample Airflow Server - Github repo
    AWS
    HuggingFace Spaces

🧭 Walkthrough: Planning an Airflow Workflow for ML Training Jobs
🧠 Why Use Airflow?

Before jumping into configuration, it's important to understand why Airflow is needed when we already have tools like Jenkins.
Key Reasons:

    Orchestration across systems: Airflow connects Jenkins, AWS EC2, and other external services in a single cohesive workflow.
    Handling asynchronous operations: Creating and using cloud resources like EC2 instances takes time. Airflow can pause and wait (poll) until those instances are ready.
    Fault tolerance and retries: Airflow can automatically retry failed tasks and gracefully handle errors without restarting the entire pipeline.
    Scheduling & monitoring: Airflow provides a centralized dashboard to monitor pipelines and run them on schedules or triggers.

    🧩 Think of Airflow as the glue that coordinates all the moving parts — ML training, testing, and deployment — across tools and platforms.

🏗️ What Will the Airflow DAG Do?

Here’s an overview of the workflow we’re about to build. This DAG (Directed Acyclic Graph) will automate the training phase of the ML pipeline:
📌 Step-by-step DAG Workflow

    Check for a successful Jenkins build
        The DAG will poll the Jenkins server to detect if a new model version has been successfully built and tested.

    Create a new EC2 instance
        Upon success, the DAG will trigger the creation of a cloud training instance on AWS.

    Wait for the EC2 to become ready
        Since cloud instances take time to initialize, the DAG will include logic to pause until the EC2 is reachable.

    Retrieve the EC2 public IP
        Once ready, the DAG will fetch the instance’s IP address to run remote commands.

    Execute the training job remotely
        The DAG connects to the EC2 instance and triggers the ML training script.

    Terminate the EC2 instance
        After training, the DAG will shut down the instance to save cloud costs.

    ✅ Airflow excels at this type of multi-step, conditional orchestration — especially when interacting with cloud services, CI/CD tools, and scripts.

🧱 Why Jenkins Alone Isn’t Enough

While Jenkins handles:

    Code integration
    Test automation
    Build pipelines

…it lacks:

    Fine-grained task scheduling
    Built-in cloud orchestration
    Retry/resume capabilities for data workflows

This is why combining Jenkins + Airflow creates a powerful MLOps architecture:

    Jenkins handles continuous integration and code testing
    Airflow manages the complex orchestration and environment setup for ML training

🔜 What’s Next?

In the next walkthrough, you’ll:

    Set up an Airflow server (e.g., using Hugging Face Spaces or local Docker)
    Write your first DAG for training orchestration
    Connect it to Jenkins and AWS

✅ Summary

You are now conceptually ready to:

    Understand the value of Airflow in ML pipelines
    Break down the steps required to automate training jobs on the cloud
    Implement a workflow that’s robust, scalable, and production-friendly

    🧠 Next time you retrain a model in production, you won’t do it manually — you’ll let Airflow handle the complexity.

🧭 Walkthrough: Setting Up Airflow and Automating ML Training with EC2 and Jenkins
🎯 Objective

By the end of this walkthrough, you will:

    Deploy an Airflow server using Docker
    Understand the configuration needed for Hugging Face Spaces
    Explore a DAG that monitors Jenkins builds, launches EC2 training jobs, and handles instance lifecycle

🪄 Step 1: Clone the Airflow Server Repository

    Go to Jedha Bootcamp GitHub
    Locate the repository: sample-airflow-server
    Copy the HTTPS URL

In your terminal:

cd ~/Desktop
git clone https://github.com/JedhaBootcamp/sample-airflow-server.git
cd sample-airflow-server
code .

🐳 Step 2: Understand and Adjust the Dockerfile

The Dockerfile contains everything needed to run Airflow on Hugging Face. Here's what it does and what you must update:
Key Configuration Details:

    Airflow base image: Official Apache Airflow Docker image is used.

    Environment Variables:
        AIRFLOW_HOME: Set to /opt/airflow
        AIRFLOW__CORE__EXECUTOR: SequentialExecutor for lightweight environments
        AIRFLOW__WEBSERVER__WEB_SERVER_PORT: Must be 7860 for Hugging Face Spaces
        AWS_DEFAULT_REGION: Set to eu-west-3 (Paris) or adjust to your region

Special Hugging Face Configurations:

    Create an airflow user with user ID 1000 (mandatory for Hugging Face Spaces)
    Configure file permissions for SSH keys using chmod 400
    Hardcode the SQL connection string due to Hugging Face's limitation with ENV vars (⚠️ Do not commit secrets to GitHub)

🔑 Step 3: Prepare SSH Keys and Secrets

Before building the server, you'll need:

    An AWS EC2 key pair (.pem file)
    A PostgreSQL URI (e.g., from Neon.tech)
    AWS credentials for programmatic EC2 access

Place your .pem file inside a folder called secrets/ in the repo root.
📊 Step 4: Review the Airflow DAG — ml_training.py

This DAG orchestrates a full ML training pipeline across Jenkins and AWS.
Workflow Summary:
Task 1: Monitor Jenkins

    Polls Jenkins API for the latest build status
    Waits for a successful build before continuing

Task 2: Create EC2 Instance

    Uses EC2CreateInstanceOperator

    Requires:
        AMI ID
        Instance type (e.g., t3.medium)
        Key name and security group

    Tags and metadata added for easy tracking

Task 3: Wait for Instance to be Ready

    Custom Python logic (Boto3) checks if:
        EC2 is in running state
        2/2 status checks have passed

Task 4: Retrieve Public IP

    Uses boto3.resource() to fetch instance details
    Extracts the public_ip_address from EC2 metadata

Task 5: Trigger Training via SSH

    Uses Paramiko to SSH into the EC2 instance
    Sets up environment variables (MLflow tracking URI, AWS credentials)
    Runs:

mlflow run https://github.com/<your-org>/<your-project> -P ...

    Captures stdout and stderr for logging

Task 6: Terminate EC2 Instance

    Uses EC2TerminateInstanceOperator to shut down the instance after training
    Uses Airflow's XCom to pass the instance ID between tasks

🧭 Walkthrough: Finalizing and Deploying Your Airflow Server on Hugging Face
🎯 Objective

In this tutorial, you will:

    Create and organize your SSH key for EC2 access
    Configure a PostgreSQL backend for Airflow using Neon.tech
    Set environment variables directly in your code
    Deploy your Airflow server to Hugging Face Spaces (private)
    Finalize security steps: password reset and repository visibility

🔑 Step 1: Create an SSH Key for EC2 Access

This key allows Airflow to SSH into an EC2 instance for remote training jobs.
1.1 Go to AWS → EC2 → Key Pairs

    Click Create key pair
    Name it something like demo-to-remove
    Format: .pem
    Type: RSA
    Click Create key pair — a .pem file will be downloaded

1.2 Organize the Key

In your terminal:

mv ~/Downloads/demo-to-remove.pem ./secrets/

Then in VS Code, verify the file exists in the secrets/ folder.
1.3 Update Dockerfile Reference

Inside your Dockerfile, make sure the path reflects the filename:

COPY secrets/demo-to-remove.pem /root/.ssh/key.pem

Also update the chmod command accordingly.
🛢 Step 2: Configure PostgreSQL with Separate Schema for Airflow

We'll use a single Neon.tech database but isolate components using schemas.
2.1 Go to Neon.tech → Open Your Project → SQL Editor

Run the following SQL commands:

CREATE SCHEMA airflow;
CREATE DATABASE airflow_db;

    💡 In production, you’d typically use separate databases, but here we use one project with multiple schemas for simplicity.

If needed, drop the database with:

DROP DATABASE airflow_db;

2.2 Update Your Connection URI

From Neon, copy the PostgreSQL connection URI and modify:

    Replace the database name with airflow_db
    Add the schema search path:

&options=-csearch_path=airflow

🔧 Full format:

postgresql://user:password@host/airflow_db?sslmode=require&options=-csearch_path=airflow

Paste this URI into your Dockerfile where AIRFLOW__CORE__SQL_ALCHEMY_CONN is set (note: this is hardcoded due to Hugging Face ENV limitations).
🛠 Step 3: Push Your Airflow Code to Hugging Face Spaces
3.1 Create a Private Space

    Go to https://huggingface.co/spaces

    Click "Create New Space"

    Fill in:
        Name: airflow-server-demo
        License: Apache 2.0
        SDK: Docker
        Hardware: Free tier
        Visibility: Private (critical – secrets are hardcoded)

    ⚠️ Make sure this repo is private. It includes hardcoded credentials and private keys.

3.2 Set Up Secrets on Hugging Face

In your Hugging Face Space:

    Go to Settings → Secrets
    Add:

Name	Value
AWS_ACCESS_KEY_ID	your AWS key
AWS_SECRET_ACCESS_KEY	your AWS secret
KEY_PAIR_PATH	path to your .pem file
SQL_ALCHEMY_CONN	your Postgres URI (hardcoded in Dockerfile)
JENKINS_USERNAME	your Jenkins username (if needed)
JENKINS_PASSWORD	your Jenkins token or password
3.3 Add Hugging Face as Git Remote

In your terminal:

git remote add hf https://huggingface.co/spaces/<your-username>/airflow-server-demo
git status
git add .
git commit -m "Ready for HF deployment"
git pull hf main --rebase
# resolve README.md conflict if prompted
git push hf main

⚙️ Step 4: Wait for the Space to Build

Go to your Hugging Face Space page. You should see a build process begin. If successful, a web interface for Airflow will appear.
🔐 Step 5: Secure Your Airflow UI
5.1 Access Airflow UI

Open your Space URL:

https://<your-username>-airflow-server-demo.hf.space

Log in using:

    Username: admin
    Password: admin

5.2 Change Your Password Immediately

    Click your profile (top right)
    Choose "Reset Password"
    Choose a strong, memorable password
    Save your changes

    🔐 Why? The default admin/admin login is insecure and your space is publicly reachable (even if your repo is private).

✅ Final Verification

You should see the jenkins_ec2_ml_training_dag already listed. If not, check:

    Your DAGs folder contains the script
    The Dockerfile points to the right location
    PostgreSQL and key path are correct

🧹 Important Best Practices

    DO NOT push this repo publicly. You have:
        Hardcoded credentials
        Sensitive SSH keys

    Use private Hugging Face Spaces for secure deployment.

    Use environment variables in real-world projects (instead of hardcoding) once Hugging Face fully supports secure runtime injection.

🧠 What You’ve Learned

You now have:

    A working Airflow server in the cloud
    SSH access to EC2 instances
    A PostgreSQL database ready to log DAG runs
    A clean and safe workflow that mimics production-grade infrastructure

🛠️ Walkthrough: Creating an EC2 AMI with MLflow and Docker Preinstalled
🎯 Objective

The goal is to create a reusable EC2 machine image (AMI) that has all necessary tools (MLflow, Docker, Python, Git) installed. This allows any new instance launched with this AMI to be ready to train ML models instantly — without repeating installation steps every time.
🧱 Step 1 – Why Use an AMI?

Before using Airflow to trigger EC2 training jobs, we need a base image with:

    MLflow preinstalled
    Docker set up properly
    Git and Python configured

    🔁 Creating this as an AMI saves you from re-installing tools via code each time you run a DAG.

🚀 Step 2 – Launch a New EC2 Instance

    Go to your AWS Console → EC2 → Launch instance

    Name it something like:

    mlflow-server-demo-to-remove

    Select Ubuntu as the OS (preferred over Amazon Linux for compatibility)

    Choose instance type:
        ✅ Recommended: T3.medium (2 vCPUs, 4GB RAM)
        ❌ Avoid: T2.micro (often fails to run MLflow reliably)

    Configure storage:
        Default is 8GB, but use 30GB to be safe

    Choose a key pair you have access to (or create one)

    Select a security group that allows SSH access from anywhere

    Click Launch instance

⏳ Step 3 – Wait for Initialization

    Go to EC2 dashboard → Instances

    Wait until the instance shows:

    Status checks: 2/2 passed

    ⏱️ Don't proceed until status is fully passed — initializing state isn't enough.

🔗 Step 4 – Connect to the EC2 Instance

Use the AWS Console “EC2 Instance Connect” to open a shell in-browser. Or, SSH in using your terminal.
🧰 Step 5 – Install System Packages

Run the following commands to prepare the environment:

sudo apt-get update
sudo apt-get install -y python3 python3-pip git
pip3 install mlflow --break-system-packages

    🧪 If mlflow isn’t recognized, update your $PATH:

export PATH="$PATH:/home/ubuntu/.local/bin"

You can verify mlflow works:

mlflow --help

🐳 Step 6 – Install Docker

    Search for “Install Docker on Ubuntu” → Open the official Docker documentation

    Run the install steps:

    sudo apt-get install \
      ca-certificates \
      curl \
      gnupg \
      lsb-release

Add Docker’s GPG key and repository:

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

Install Docker Engine:

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

Add your user to the Docker group:

sudo usermod -aG docker $USER
newgrp docker

    This avoids permission errors when running docker without sudo.

✅ Step 7 – Test MLflow Training Locally

Set your environment variables:

export MLFLOW_TRACKING_URI=https://yourusername-mlflow-server-demo.hf.space
export MLFLOW_EXPERIMENT_ID=1  # or whatever your experiment ID is
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

Then run your training command:

mlflow run https://github.com/yourusername/yourrepo -P config=hyperopt.yaml

Make sure:

    MLflow logs appear
    Docker runs the training
    Results show up in your MLflow dashboard

🧊 Step 8 – Create the AMI

Once confirmed working:

    Go to EC2 dashboard → Select your instance

    Click Actions > Image and templates > Create image

    Name it:

    mlflow-server-demo

Add a description:

AMI with MLflow, Docker, Git, Python3 installed

    Click Create image

    Go to Images > AMIs and wait for the status to become available

    ⚠️ Important: Do not stop or terminate the instance while the AMI is being created.

💾 Step 9 – Save Your AMI ID

Copy and save the AMI ID somewhere safe. You’ll need it in your Airflow DAG to specify which image to use when launching new EC2 instances.
🏁 You're Done!

Your custom AMI is now ready. It’s reusable and preconfigured — making your training jobs reproducible, quick to launch, and less prone to runtime errors. You may now delete your EC2 instance.
🧠 In Practice

In real-world ML engineering:

    Teams maintain prebuilt training environments via AMIs or Docker images
    Airflow DAGs launch those environments on demand
    This guarantees consistency and saves massive setup time

✅ Walkthrough: Finalizing and Running Your Airflow DAG with Jenkins and EC2
🎯 Goal

You will:

    Set all required environment variables in Airflow
    Configure AWS credentials in Airflow connections
    Trigger your final DAG
    Confirm that it launches a Jenkins build, spins up an EC2 instance, and runs an MLflow training job via SSH

🗂 Step 1 – Gather the Required Environment Variables

Here’s the list of environment variables you’ll need to define in Airflow:
Variable	Description
JENKINS_URL	Your Jenkins server's URL (e.g., via ngrok)
JENKINS_USER	Jenkins username
JENKINS_TOKEN	Jenkins API token
JENKINS_JOB_NAME	The name of the Jenkins job (e.g., grid-search-demo), use the name you used for the demo job in Jenkins
AWS_ACCESS_KEY_ID	Your AWS access key
AWS_SECRET_ACCESS_KEY	Your AWS secret key
AMI_ID	The ID of your custom EC2 AMI
KEY_PAIR_NAME	Name of the EC2 SSH key pair
KEY_PATH	Path to your SSH key in the Docker container (/opt/airflow/demo-to-remove.pem)
SECURITY_GROUP_ID	ID of the security group used by your EC2 instance
INSTANCE_TYPE	e.g., t3.medium
MLFLOW_TRACKING_URI	Your MLflow tracking server URL
MLFLOW_EXPERIMENT_ID	Experiment ID in MLflow (ensure it’s the correct one)
📝 Step 2 – Create a JSON File for Airflow Variables

Create a file called variables.json with the following structure:

{
  "JENKINS_URL": "https://your-ngrok-url.ngrok.io",
  "JENKINS_USER": "admin",
  "JENKINS_TOKEN": "your-token",
  "JENKINS_JOB_NAME": "GridSearchDemo",
  "AWS_ACCESS_KEY_ID": "your-access-key",
  "AWS_SECRET_ACCESS_KEY": "your-secret-key",
  "AMI_ID": "ami-1234567890abcdef0",
  "KEY_PAIR_NAME": "demo-to-remove",
  "KEY_PATH": "/opt/airflow/demo-to-remove.pem",
  "SECURITY_GROUP_ID": "sg-1234567890abcdef0",
  "INSTANCE_TYPE": "t3.medium",
  "MLFLOW_TRACKING_URI": "https://your-mlflow-server.hf.space",
  "MLFLOW_EXPERIMENT_ID": "1"
}

Make sure every value is up to date and valid.
🧭 Step 3 – Upload and Import Variables in Airflow

    Open your Airflow web UI
    Go to Admin > Variables
    Click Import Variables
    Select and upload variables.json
    Confirm successful import

    ✅ You can verify the values by browsing through the variable list in the UI.

🔐 Step 4 – Set AWS Credentials in Airflow Connections

    Go to Admin > Connections

    Find the connection with Conn ID = aws_default

    Click Edit

    Set:
        Access Key ID → your AWS access key
        Secret Access Key → your AWS secret

    Click Save

    ⏳ Wait for the page to fully load before editing — otherwise, you won’t see all input fields.

▶️ Step 5 – Trigger the DAG

    In the DAGs view, find your DAG (e.g., jenkins_ec2_training_dag)
    Click the play icon to trigger it
    Monitor progress using the DAG graph view or logs

🔍 Step 6 – Observe and Debug the Process

Check each task in the DAG:

    Get Jenkins Build Info ✅ Should return green — confirms connection to Jenkins is working

    Create EC2 Instance ✅ Instance will show up in AWS Console → EC2 → Instances

    Wait for Instance Status 🔁 Loops until the instance is fully running (2/2 checks passed)

    Get EC2 Public IP ✅ Needed for SSH connection

    Run Training via Paramiko (SSH) ✅ Uses Paramiko to SSH into the instance and run the MLflow training command

    🧠 If this step fails with No experiment with id=1, double-check your MLFLOW_EXPERIMENT_ID variable.

🧪 Step 7 – Check Your Results in MLflow

    Open your MLflow tracking server
    Go to the specified experiment (e.g., ID = 1)
    Confirm that a new run appears, triggered from the EC2 instance

    🟢 If it's there: congratulations, everything is working!

🧹 Step 8 – Confirm EC2 Termination

After the DAG finishes:

    Go to AWS → EC2 → Instances
    The instance should automatically terminate
    If it doesn’t, ensure the termination step is part of your DAG

🚀 Bonus – What’s Next?

Now that you have a fully working pipeline:

    Add scheduling to the DAG to run it daily or hourly
    Connect a GitHub webhook to auto-trigger the Jenkins build on new commits
    Use conditionals to trigger retraining based on data drift or accuracy drop

🎉 Final Words

You’ve now completed a full production-ready MLOps pipeline:

    CI/CD via Jenkins
    Workflow orchestration with Airflow
    Remote training on EC2
    Experiment tracking via MLflow

👏 Great job! You’ve implemented core principles of real-world ML engineering and MLOps.
Congrats 🥳 🎉

Congratulations, if you are at that step, you made something huge!!
Resources 📚📚

    Airflow
